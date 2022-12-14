from rest_framework import serializers
from .models import  Book
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['_id', 'barcode', 'name', 'is_reserved', 'is_deleted', 'user_id', 'return_date', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined']