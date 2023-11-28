from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from drf_spectacular.utils import extend_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "phone": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email", "password", "first_name", "last_name"],
        ),
        responses={
            201: openapi.Response(
                description="User created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    @extend_schema(
        summary="Register",
        description="Register a new user.",
        request=RegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def post(self, request):
        User = get_user_model()

        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone = request.data.get("phone")

        if not email or not password or not first_name or not last_name:
            return Response(
                {"error": "Email, password, first_name and last_name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validate_email(email):
            return Response(
                {"error": "Email is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(
            token_data,
            status=status.HTTP_201_CREATED,
        )
