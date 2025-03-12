from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    book_list,
    approve_request,
    request_borrow,
    return_book,
    signup_view,
    login_view,
    custom_logout,
    admin_dashboard,
    admin_login,
    admin_logout,
    add_book,
    upload_books,
)

# app_name = "books"

urlpatterns = [
    path('', book_list, name='book_list'),

    # User Authentication
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),

    # Admin Authentication
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    # Admin dashboard & book management
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Keep only this
    path('add_book/', add_book, name='add_book'),
    path('upload_books/', upload_books, name='upload_books'),

    # Borrow & Return
    path('request_borrow/<int:book_id>/', request_borrow, name='request_borrow'),
    path('return_book/<int:book_id>/', return_book, name='return_book'),
    path('approve_request/<int:request_id>/', approve_request, name='approve_request'),

    # Search bar
    path('', book_list, name='book_list'),

]

