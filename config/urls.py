from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

from core import views

admin.site.site_url = settings.FRONTEND_HOST

schema_view = get_schema_view(
    openapi.Info(
        title="Wasted-app API",
        default_version="v1",
        description="API for Wasted-app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
    authentication_classes=(views.BearerTokenAuthentication, SessionAuthentication),
)

urlpatterns = [
    path("swagger(<format>\.json|\.yaml)", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # noqa
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # noqa
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),  # noqa
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("categories_groups/", views.CategoryGroupView.as_view(), name="categories"),
    path("categories/", views.CategoryView.as_view(), name="categories"),
    path("wastes/", views.WasteView.as_view(), name="wastes"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
