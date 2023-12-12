from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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


from rest_framework_simplejwt.views import TokenRefreshView

from .views.addperms import *
from .views.logout import *
from .views.protectedfile import *
from .views.register import *
from .views.whoami import *

urlpatterns = [
    # YOUR PATTERNS
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
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
    path("api/polls/", include("rodManager.views.polls.urls")),
    path("api/my-garden/", include("rodManager.views.myGardenPlot.urls")),
    path("api/garden-info/", include("rodManager.views.RODInfo.urls")),
    path("api/technical-problem/", include("rodManager.views.technicalProblem.urls")),
    path("api/who-am-i/", WhoamiView.as_view(), name="whoami"),
    path("api/payments/", include("rodManager.views.payments.urls")),
    path("api/manager-documents/", include("rodManager.views.managerdocuments.urls")),
    path("api/user-documents/", include("rodManager.views.userdocuments.urls")),
    path("api/rod-documents/", include("rodManager.views.roddocuments.urls")),
    path("api/complaints/", include("rodManager.views.complaints.urls")),
    path("api/notifications/", include("rodManager.views.notifications.urls")),
    path("api/gardeneirs/", include("rodManager.views.gardeneirs.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
