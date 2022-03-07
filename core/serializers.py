from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, CategoryGroup


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
        )
        return user

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name"]


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGroup
        fields = "__all__"
