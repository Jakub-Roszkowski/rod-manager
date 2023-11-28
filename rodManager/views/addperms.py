from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.users.validate import permission_required


class AddPermsRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()


class AddPermsView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=AddPermsRequestSerializer,
        summary="Add user to group",
        responses={
            201: OpenApiResponse(description="Group added successfully"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    @permission_required("rodManager.change_account")
    def post(self, request: Request):
        User = get_user_model()
        serializer = AddPermsRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            role = serializer.validated_data.get("role")

            if not Group.objects.filter(name=role).exists():
                return Response(
                    {"error": "Role does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            group = Group.objects.get(name=role)

            user = User.objects.get(email=email)
            if (
                request.user.groups.filter(name="MANAGER").exists()
                and not request.user.groups.filter(name="ADMIN").exists()
            ):
                if role in ("MANAGER", "ADMIN"):
                    return Response(
                        {"error": "You cannot add managers or admins."}, status=400
                    )
            user.groups.add(group)
            user.save()

            return Response(
                {"success": "Role added successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
