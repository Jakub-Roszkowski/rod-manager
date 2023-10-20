from django.urls import path

# from . import views
from .views.register import *
from .views.login import *
from .views.logout import *

urlpatterns = [
    # path("", views.index, name="index"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
