from django.urls import path
from .views import (
    # Web views
    home_view, student_book_list, signup_view, login_view, logout_view,
    dashboard_view, edit_book, delete_book,
    
    # API views (DRF)
    AdminSignupView, AdminLoginView,
    BookCreateView, BookListView, BookUpdateView,
    BookDeleteView, StudentBookListView
)

urlpatterns = [
    # 🌐 Web UI Routes
    path('', home_view, name='home'),
    path('books/', student_book_list, name='book-list'),  # Login required
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('edit/<int:pk>/', edit_book, name='edit-book'),
    path('delete/<int:pk>/', delete_book, name='delete-book'),

    # 🔗 API Routes (Django REST Framework)
    path('api/admin/signup/', AdminSignupView.as_view(), name='api-admin-signup'),
    path('api/admin/login/', AdminLoginView.as_view(), name='api-admin-login'),
    path('api/books/create/', BookCreateView.as_view(), name='api-book-create'),
    path('api/books/', BookListView.as_view(), name='api-book-list'),
    path('api/books/update/<int:id>/', BookUpdateView.as_view(), name='api-book-update'),
    path('api/books/delete/<int:id>/', BookDeleteView.as_view(), name='api-book-delete'),

    # 👨‍🎓 Public API (Student book list)
    path('api/student/books/', StudentBookListView.as_view(), name='api-student-book-list'),
]
