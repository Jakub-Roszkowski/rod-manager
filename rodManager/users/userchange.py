from django.contrib.auth.forms import UserChangeForm
from django.forms import EmailField
from rodManager.dir_models.account import Account

class CustomUserChangeForm(UserChangeForm): 
    class Meta(UserChangeForm.Meta):
        model = Account
        fields = UserChangeForm.Meta.fields
        field_classes = {"email": EmailField, }