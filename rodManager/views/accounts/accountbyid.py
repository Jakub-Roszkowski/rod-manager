from django.contrib.auth.models import Group
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.users.validate import permission_required


class UpdateAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(allow_null=True, required=False)
    groups = serializers.ListField(child=serializers.CharField(), required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        group_names = validated_data.get("groups")
        if group_names is not None:
            groups = Group.objects.filter(name__in=group_names)
            if len(groups) != len(group_names):
                raise serializers.ValidationError("One or more groups do not exist.")
            instance.groups.set(groups)
        instance.save()
        return instance


class AccountByIdView(APIView):
    @extend_schema(
        summary="Get account by id",
        responses={
            200: OpenApiResponse(
                description="Accounts",
                response={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "groups": {
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
    @permission_required()
    def get(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            response_data = {
                "id": account.id,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email,
                "phone": account.phone,
                "groups": [group.name for group in account.groups.all()],
            }

            if (
                not request.user.groups.filter(name__in=["MANAGER", "ADMIN"]).exists()
                and request.user != account
            ):
                return Response({"error": "You cannot view this account."}, status=400)

            return Response(response_data)
        except Account.DoesNotExist:
            return Response({"error": "Account does not exist."}, status=400)

    @extend_schema(
        request=UpdateAccountSerializer,
        summary="Update account",
        responses={
            200: OpenApiResponse(
                description="Account updated successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "groups": {
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
    @permission_required()
    def patch(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            if (
                account.groups.filter(name__in=["MANAGER", "ADMIN"]).exists()
                and not request.user.groups.filter(name="ADMIN").exists()
                and account != request.user
            ) or (
                account != request.user
                and not request.user.groups.filter(
                    name__in=["MANAGER", "ADMIN"]
                ).exists()
            ):
                return Response({"error": "You cannot edit this account."}, status=400)
            serializer = UpdateAccountSerializer(
                instance=account, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            account.refresh_from_db()

            response_data = {
                "id": account.id,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email,
                "phone": account.phone,
                "groups": [group.name for group in account.groups.all()],
            }

            return Response(response_data)
        except Account.DoesNotExist:
            return Response({"error": "Account does not exist."}, status=400)
