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
        default_version='v1',
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
    path(r"swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(r"swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(r"signup/", views.SignUpView.as_view(), name="signup"),
    path(r"login/", views.LoginView.as_view(), name="login"),
    path(r"categories/", views.CategoryView.as_view(), name="categories"),
    path(r"categories_groups/", views.CategoryView.as_view(), name="categories"),
    # path(r"^partners/?$", views.PartnerView.as_view(), name="partners"),
    # path(r"^tasks/?$", views.TaskView.as_view(), name="tasks"),
    # path(r"^points/?$", views.PointView.as_view(), name="points"),
    # path(r"^edit_point/?$", views.EditPointView.as_view(), name="edit_point"),
    # path(r"^moderate_task/?$", views.ModerateTaskView.as_view(), name="moderate_task"),
    # path(r"^profile/?$", views.ProfileView.as_view(), name="profile"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
