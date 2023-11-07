from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth.models import Group


class AddPermsView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "role": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email", "role"],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Group added successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
        },
    )
    def post(self, request: Request):
        User = get_user_model()

        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        role = request.data.get("role")

        if not role:
            return Response(
                {"error": "Role is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group = Group.objects.get(name=role)

        if not group:
            return Response(
                {"error": "Role does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        user.groups.add(group)
        user.save()

        return Response(
            {"success": "Role added successfully."},
            status=status.HTTP_201_CREATED,
        )
