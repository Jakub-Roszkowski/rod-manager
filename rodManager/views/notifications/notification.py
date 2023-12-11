from django.db import models
from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.notification import Notification
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class AddNotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    type = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    text = serializers.CharField(required=True)

    class Meta:
        model = Notification
        fields = [
            "user",
            "type",
            "date",
            "text",
        ]

    def create(self, validated_data):
        notification = Notification.objects.create(
            user=validated_data["user"],
            type=validated_data["type"],
            date=validated_data["date"],
            text=validated_data["text"],
        )
        notification.save()
        return notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "type", "date", "text", "is_read"]


class NotificationView(APIView):
    pagination_class = RODPagination

    @extend_schema(
        summary="Get notifications for actual user",
        description="Get notifications for actual user.",
        parameters=[
            OpenApiParameter(
                name="only_unread",
                description="Show only unread notifications",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses=NotificationSerializer(many=True),
    )
    @permission_required()
    def get(self, request):
        paginator = RODPagination()
        if request.GET.get("only_unread") == "true":
            notifications = paginator.paginate_queryset(
                Notification.objects.filter(user=request.user, is_read=False).order_by(
                    "-date"
                ),
                request,
            )
        else:
            notifications = paginator.paginate_queryset(
                Notification.objects.filter(user=request.user).order_by("-date"),
                request,
            )
        return paginator.get_paginated_response(
            NotificationSerializer(notifications, many=True).data
        )

    @extend_schema(
        summary="Add notification",
        description="Add notification in the system. (ONLY FOR TESTING, NOT FOR PRODUCTION)",
        request=AddNotificationSerializer,
        responses=NotificationSerializer(),
    )
    @permission_required()
    def post(self, request):
        serializer = AddNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
