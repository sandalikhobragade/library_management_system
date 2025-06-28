# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom Admin User
class AdminManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Admin must have an email")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'

    objects = AdminManager()

    def __str__(self):
        return self.email

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title
