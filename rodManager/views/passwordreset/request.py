import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rodManager.dir_models.account import Account
from rodManager.dir_models.passwordreset import PasswordReset
from rodManager.libs.mailsending import send_mail_from_template


class PaswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PaswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Password reset request",
        description="Password reset request.",
        request=PaswordResetRequestSerializer,
        responses={
            201: OpenApiResponse(
                description="Password reset request created successfully.",
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
        if request.data.get("email") is None:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Account.objects.filter(email=request.data.get("email")).exists():
            return Response(
                {"error": "Email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = Account.objects.get(email=request.data.get("email"))

        PasswordReset.objects.filter(user=user).delete()
        PasswordReset.objects.filter(valid_until__lt=timezone.now()).delete()
        token = uuid.uuid4()
        request = PasswordReset.objects.create(
            user=user,
            valid_until=timezone.now() + timedelta(days=1),
            token=token,
        )
        request.save()
        send_mail_from_template(
            "password_reset",
            "Reset hasła",
            [
                "tomek@plociennik.info"
            ],  # TODO zmienić maila na user.email, ale aktualnie maile to np. admin@admin.admin więc nie działa
            {
                "link": "http://localhost:4200/password-reset/" + str(request.token),
            },
        )
        return Response({"ok": "Request created successfully."})
