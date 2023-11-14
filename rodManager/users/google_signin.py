from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from django.contrib.auth.models import Group
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleTokenLogin(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "token": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["token"],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response("Login successful"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
        },
    )
    def post(self, request):
        User = get_user_model()

        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )

        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            return Response(
                {"error": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = idinfo["email"]

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_200_OK,
            )
        else:
            User.objects.create_user(
                email=email,
                first_name=idinfo["given_name"],
                last_name=idinfo["family_name"],
                google_auth=True,
            )
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=status.HTTP_200_OK,
            )
