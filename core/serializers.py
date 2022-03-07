from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, CategoryGroup, Waste


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
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
        fields = ("email", "password")


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class CategoryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGroup
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    category_group = CategoryGroupSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        exclude = ("user",)


class WasteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Waste
        exclude = ("user",)


class CreateWasteSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Waste
        exclude = ("user", "category")


class UpdateWasteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    category_id = serializers.IntegerField(required=False)
    amount = serializers.FloatField(required=False)
    name = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs.pop("id")
        if not attrs:
            raise serializers.ValidationError("Any of 'category_id', 'amount' or 'name' required")
        return attrs

    class Meta:
        model = Waste
        exclude = ("user", "category")


class DeleteWasteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Waste
        fields = ("id",)
