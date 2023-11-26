from django.contrib.auth.models import Group
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   OpenApiTypes, extend_schema,
                                   inline_serializer)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account


class UpdateAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(allow_null=True, required=False)
    groups = serializers.ListField(child=serializers.CharField(), required=False)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        group_names = validated_data.get('groups')
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

            return Response(response_data)
        except Account.DoesNotExist:
            return Response({"error": "Account does not exist."}, status=400)

    @extend_schema(
        request=UpdateAccountSerializer,
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
    def put(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)

            serializer = UpdateAccountSerializer(instance=account, data=request.data, partial=True)
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
