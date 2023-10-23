from rest_framework_simplejwt.views import  TokenObtainPairView
from dir_models.account import Account

class CustomLogin(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        roles = Account.objects.get(email=request.data['email']).groups
        response.data['roles'] = [role.name for role in roles.all()]
        return response