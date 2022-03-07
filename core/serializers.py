from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, CategoryGroup


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = ["email", "password"]


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGroup
        fields = "__all__"
