import uuid

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rodManager.dir_models.account import Account
from rodManager.dir_models.passwordreset import PasswordReset
from rodManager.libs.mailsending import send_mail_from_template


class PaswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PaswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Password reset confirm",
        description="Password reset confirm.",
        request=PaswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(
                description="Password changed successfully.",
                response={
                    "type": "object",
                    "properties": {"ok": {"type": "string"}},
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
    def post(self, request):
        if request.data.get("token") is None:
            return Response(
                {"error": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("password") is None:
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        PasswordReset.objects.filter(valid_until__lt=timezone.now()).delete()
        if not PasswordReset.objects.filter(token=request.data.get("token")).exists():
            return Response(
                {"error": "Token expired or does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        passwordreset = PasswordReset.objects.get(token=request.data.get("token"))
        user = passwordreset.user
        user.set_password(request.data.get("password"))
        user.save()
        passwordreset.delete()
        return Response({"ok": "Password changed successfully."})
