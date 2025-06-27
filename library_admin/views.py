from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from users.models import Book, Transaction, UserProfile
from .forms import BookForm, UserEditForm, UserCreateForm


def is_admin(user):
    return user.is_staff or user.is_superuser


# Custom admin login view
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('library_admin:admin_dashboard')
            else:
                messages.error(request, 'Access denied. Admin privileges required.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'library_admin/admin_login.html')


@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_books = Book.objects.count()
    total_users = User.objects.count()
    active_transactions = Transaction.objects.filter(transaction_status='borrowed').count()
    overdue_transactions = Transaction.objects.filter(
        transaction_status='borrowed',
        due_date__lt=timezone.now()
    ).count()

    recent_transactions = Transaction.objects.all().order_by('-borrow_date')[:10]

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'active_transactions': active_transactions,
        'overdue_transactions': overdue_transactions,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'library_admin/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def manage_books_view(request):
    books = Book.objects.all().order_by('-date_added')
    return render(request, 'library_admin/manage_books.html', {'books': books})


@login_required
@user_passes_test(is_admin)
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('library_admin:manage_books')
    else:
        form = BookForm()
    return render(request, 'library_admin/add_book.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('library_admin:manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'library_admin/edit_book.html', {'form': form, 'book': book})


@login_required
@user_passes_test(is_admin)
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
    return redirect('library_admin:manage_books')


# ENHANCED USER MANAGEMENT WITH CRUD OPERATIONS

@login_required
@user_passes_test(is_admin)
def manage_users_view(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library_admin/manage_users.html', {
        'users': page_obj,
        'total_users': users.count()
    })


@login_required
@user_passes_test(is_admin)
def add_user_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully!')
            return redirect('library_admin:manage_users')
    else:
        form = UserCreateForm()
    return render(request, 'library_admin/add_user.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_user_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user_obj.username}" updated successfully!')
            return redirect('library_admin:manage_users')
    else:
        form = UserEditForm(instance=user_obj)
    return render(request, 'library_admin/edit_user.html', {'form': form, 'user_obj': user_obj})


@login_required
@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if user_obj.is_superuser:
            messages.error(request, 'Cannot delete superuser!')
        elif user_obj == request.user:
            messages.error(request, 'Cannot delete your own account!')
        else:
            username = user_obj.username
            user_obj.delete()
            messages.success(request, f'User "{username}" deleted successfully!')
    return redirect('library_admin:manage_users')


@login_required
@user_passes_test(is_admin)
def toggle_user_status_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status = "activated" if user_obj.is_active else "deactivated"
        messages.success(request, f'User "{user_obj.username}" {status} successfully!')
    return redirect('library_admin:manage_users')


@login_required
@user_passes_test(is_admin)
def manage_transactions_view(request):
    transactions = Transaction.objects.all().order_by('-borrow_date')
    return render(request, 'library_admin/manage_transactions.html', {
        'transactions': transactions,
        'today': timezone.now().date()
    })