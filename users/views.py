from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Book, Transaction, UserProfile
from .forms import UserRegistrationForm, BookSearchForm, ProfileEditForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Welcome {user.first_name}! Registration successful!')
                return redirect('users:dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    """View user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Get user statistics
    total_borrowed = Transaction.objects.filter(user=request.user).count()
    currently_borrowed = Transaction.objects.filter(user=request.user, transaction_status='borrowed').count()
    books_returned = Transaction.objects.filter(user=request.user, transaction_status='returned').count()

    context = {
        'profile': profile,
        'total_borrowed': total_borrowed,
        'currently_borrowed': currently_borrowed,
        'books_returned': books_returned,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Update user information
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Update profile information
            form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard_view(request):
    recent_books = Book.objects.filter(availability_status=True)[:6]
    user_transactions = Transaction.objects.filter(user=request.user)[:5]
    return render(request, 'users/dashboard.html', {
        'recent_books': recent_books,
        'user_transactions': user_transactions
    })


@login_required
def book_list_view(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        search_by = form.cleaned_data.get('search_by')

        if query:
            if search_by == 'title':
                books = books.filter(book_title__icontains=query)
            elif search_by == 'author':
                books = books.filter(book_author__icontains=query)
            elif search_by == 'year':
                try:
                    year = int(query)
                    books = books.filter(publication_year=year)
                except ValueError:
                    books = books.none()

    return render(request, 'users/book_list.html', {
        'books': books,
        'form': form
    })


@login_required
def borrow_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.availability_status:
        messages.error(request, 'This book is not available.')
        return redirect('users:book_list')

    existing_transaction = Transaction.objects.filter(
        user=request.user,
        book=book,
        transaction_status='borrowed'
    ).exists()

    if existing_transaction:
        messages.error(request, 'You have already borrowed this book.')
        return redirect('users:book_list')

    due_date = timezone.now() + timedelta(days=6)
    Transaction.objects.create(
        user=request.user,
        book=book,
        book_title=book.book_title,
        due_date=due_date
    )

    if book.book_copies > 1:
        book.book_copies -= 1
    else:
        book.availability_status = False
    book.save()

    messages.success(request, f'You have successfully borrowed "{book.book_title}".')
    return redirect('users:borrowed_books')


@login_required
def borrowed_books_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'users/borrowed_books.html', {'transactions': transactions})


@login_required
def return_book_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if transaction.transaction_status != 'borrowed':
        messages.error(request, 'This book has already been returned.')
        return redirect('users:borrowed_books')

    transaction.return_date = timezone.now()
    transaction.transaction_status = 'returned'
    transaction.save()

    book = transaction.book
    book.book_copies += 1
    book.availability_status = True
    book.save()

    messages.success(request, f'You have successfully returned "{transaction.book_title}".')
    return redirect('users:borrowed_books')