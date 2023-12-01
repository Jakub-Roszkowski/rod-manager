from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from ..dir_models.account import Account


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CustomLogin(TokenObtainPairView):
    @extend_schema(
        summary="Login",
        description="Login to the system.",
        request=CustomLoginSerializer,
        responses={
            200: OpenApiResponse(
                description="Login successful.",
                response={
                    "type": "object",
                    "properties": {
                        "refresh": {"type": "string"},
                        "access": {"type": "string"},
                        "roles": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            ),
            400: OpenApiResponse(
                description="Bad request.",
                response={
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        roles = Account.objects.get(email=request.data["email"]).groups
        response.data["roles"] = [role.name for role in roles.all()]
        return response
