from django.contrib import admin
from .models import Book, AdminUser

admin.site.register(Book)
admin.site.register(AdminUser)
