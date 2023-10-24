from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegistrationView(APIView):
    class RegistrationView(APIView):
        permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "surname": openapi.Schema(type=openapi.TYPE_STRING),
                "phone": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "password", "name", "surname"],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Registration successful"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
        },
    )
    def post(self, request):
        User = get_user_model()
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        surname = request.data.get("surname")
        phone = request.data.get("phone")

        if not email or not password or not name or not surname:
            return Response(
                {"error": "Email, password, name and surname are required."},
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
            email=email,
            password=password,
            first_name=name,
            last_name=surname,
            phone=phone,
        )
        return Response(
            {"message": "Registration successful."}, status=status.HTTP_201_CREATED
        )
