from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Category, CategoryGroup, Waste
from .serializers import (
    CategoryGroupSerializer,
    CategorySerializer,
    CreateWasteSerializer,
    DeleteWasteSerializer, LogInSerializer,
    SignUpSerializer,
    UpdateWasteSerializer,
    WasteSerializer,
)


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class SignUpView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        headers = self.get_success_headers(serializer.data)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": user.username},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(generics.CreateAPIView):
    serializer_class = LogInSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "username": username},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryGroupView(generics.ListAPIView):
    queryset = CategoryGroup.objects.all()
    serializer_class = CategoryGroupSerializer
    permission_classes = [permissions.AllowAny]


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user,
        ).select_related("category_group")


class WasteView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.ListCreateAPIView):
    serializer_class = WasteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Waste.objects.filter(
            user=self.request.user,
        ).select_related("category__category_group")

    @swagger_auto_schema(request_body=CreateWasteSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CreateWasteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = self.request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(request_body=UpdateWasteSerializer)
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        try:
            instance = Waste.objects.get(id=request.data.get("id"), user=self.request.user)
        except Waste.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateWasteSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            category_id = serializer.validated_data.get("category_id")
            category_id and Category.objects.get(id=category_id, user=self.request.user)
        except Category.DoesNotExist:
            return Response("Category not found", status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data["user"] = self.request.user
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(request_body=DeleteWasteSerializer)
    def delete(self, request, *args, **kwargs):
        try:
            instance = Waste.objects.get(id=request.data.get("id"), user=self.request.user)
        except Waste.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
