from rest_framework import serializers
from .models import AdminUser, Book

# ✅ Admin Signup Serializer (used for signup)
class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminUser
        fields = ['email', 'password']

    def create(self, validated_data):
        user = AdminUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# ✅ Book Serializer (required for Book CRUD)
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
