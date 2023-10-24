from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField
from rodManager.dir_models.account import Account


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("email", "first_name", "last_name", "phone")
        fields_classes = {"email": EmailField, "first_name": CharField, "last_name": CharField, "phone": CharField}