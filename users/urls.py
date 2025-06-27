from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('books/', views.book_list_view, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book_view, name='borrow_book'),
    path('borrowed/', views.borrowed_books_view, name='borrowed_books'),
    path('return/<int:transaction_id>/', views.return_book_view, name='return_book'),

    # Profile management
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]