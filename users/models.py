from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_contact = models.CharField(max_length=15, blank=True, null=True)  # Allow blank
    user_address = models.TextField(blank=True, null=True)  # Allow blank
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    book_copies = models.IntegerField(default=1)
    publication_year = models.IntegerField()
    publication_name = models.CharField(max_length=100)
    book_isbn = models.CharField(max_length=13, unique=True)
    date_added = models.DateTimeField(default=timezone.now)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.book_title

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    transaction_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.user.username} - {self.book_title}"