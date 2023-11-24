from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rodManager.users.google_signin import GoogleTokenLogin

from rodManager.views.tokenobtain import CustomLogin

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# from . import views


from .views.register import *
from .views.logout import *
from .views.addperms import *
from .views.announcements.image import *
from .views.announcements.tags import *
from .views.protectedfile import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/login/", CustomLogin.as_view(), name="token_obtain_pair"),
    path("api/register/", RegistrationView.as_view(), name="register"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/image/", ImageView.as_view(), name="image"),
    path("api/login/google/", GoogleTokenLogin.as_view(), name="google_login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/addperms/", AddPermsView.as_view(), name="addperms"),
    path("api/tag/", TagView.as_view(), name="tag"),
    path(
        "api/protectedfile/<str:file_id>",
        ProtectedFileView.as_view(),
        name="protectedfile",
    ),
    path("api/garden/", include("rodManager.views.gardens.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
