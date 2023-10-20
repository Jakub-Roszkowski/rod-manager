from django.urls import path, include

# from . import views


from .views.register import *
from .views.login import *
from .views.logout import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/register', RegistrationView.as_view(), name='register'),
    path('api/login', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]