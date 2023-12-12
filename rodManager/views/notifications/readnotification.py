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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "type", "date", "text", "is_read"]


class ReadNotificationView(APIView):
    @extend_schema(
        summary="Mark notification as read",
        description="Mark notification as read.",
        responses=NotificationSerializer(),
    )
    @permission_required()
    def post(self, request, notification_id):
        notification = Notification.objects.get(id=notification_id)
        if notification is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Notification not found."},
            )
        if notification.user != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    "detail": "You cannot mark this notification as read. (wrong user)"
                },
            )
        if notification.is_read:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "This notification is already marked as read."},
            )
        notification.is_read = True
        notification.save()
        return Response(
            NotificationSerializer(notification).data, status=status.HTTP_200_OK
        )
