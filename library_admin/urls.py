from django.urls import path
from . import views

app_name = 'library_admin'

urlpatterns = [
    # Custom admin login
    path('login/', views.admin_login_view, name='admin_login'),

    # Dashboard
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    # Book management
    path('books/', views.manage_books_view, name='manage_books'),
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book_view, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book_view, name='delete_book'),

    # User management with CRUD
    path('users/', views.manage_users_view, name='manage_users'),
    path('users/add/', views.add_user_view, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status_view, name='toggle_user_status'),

    # Transaction management
    path('transactions/', views.manage_transactions_view, name='manage_transactions'),
]