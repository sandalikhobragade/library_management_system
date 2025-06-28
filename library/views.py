# Django REST Framework (API Views)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from .serializers import AdminSignupSerializer, BookSerializer
from .models import AdminUser, Book

# ✅ API: Signup
class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ API: Login
class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ Custom permission for authenticated admin
class IsAdminAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

# ✅ API: Book CRUD
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminAuthenticated]

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminAuthenticated]
    lookup_field = 'id'

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminAuthenticated]
    lookup_field = 'id'

# ✅ API: Student public view (REST API for /api/student/books/)
class StudentBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Public access

# -----------------------------------------
# Web Views for UI Templates (HTML Pages)
# -----------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AdminSignupForm, AdminLoginForm, BookForm

# 🏠 Home
def home_view(request):
    return render(request, 'home.html')

# 📚 Student Book List — NOW RESTRICTED!
@login_required(login_url='/login/')
def student_book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# 🔐 Admin Signup
def signup_view(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash
            user.save()
            messages.success(request, "✅ Signup successful! Please log in.")
            return redirect('login')
    else:
        form = AdminSignupForm()
    return render(request, 'signup.html', {'form': form})

# 🔑 Admin Login
def login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, "✅ Login successful.")
                return redirect('dashboard')
            else:
                messages.error(request, "🚫 Invalid login credentials.")
    else:
        form = AdminLoginForm()
    return render(request, 'login.html', {'form': form})

# 🔓 Admin Logout
def logout_view(request):
    logout(request)
    messages.info(request, "ℹ️ Logged out.")
    return redirect('home')

# 🧑‍💼 Admin Dashboard (Create Book)
@login_required(login_url='/login/')
def dashboard_view(request):
    books = Book.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Book added.")
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'dashboard.html', {'books': books, 'form': form})

# ✏️ Edit Book
@login_required(login_url='/login/')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "✅ Book updated.")
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'form': form, 'books': Book.objects.all()})

# ❌ Delete Book
@login_required(login_url='/login/')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, "🗑️ Book deleted.")
    return redirect('dashboard')
