from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

from rodManager.users.google_signin import GoogleTokenLogin
from rodManager.views.login import CustomLogin

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


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.addperms import *
from .views.logout import *
from .views.protectedfile import *
from .views.register import *

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
    path("api/login/google/", GoogleTokenLogin.as_view(), name="google_login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/addperms/", AddPermsView.as_view(), name="addperms"),
    re_path(
        r"^api/protectedfile/(?P<file_path>.+)$",
        ProtectedFileView.as_view(),
        name="protectedfile",
    ),
    path("api/gardens/", include("rodManager.views.gardens.urls")),
    path("api/garden-offers/", include("rodManager.views.gardenoffers.urls")),
    path("api/announcements/", include("rodManager.views.announcements.urls")),
    path("api/accounts/", include("rodManager.views.accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
