import django.utils.timezone
from django.db import models
from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_field,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.dir_models.complaint import (
    Complaint,
    ComplaintSerializer,
    MessageAuthor,
)
from rodManager.dir_models.notification import Notification
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class NewNotificationView(APIView):
    @extend_schema(
        summary="Get count of new notifications for actual user",
        description="Managers gets full response, users gets only count of new notifications and new complaints.",
        responses={
            200: OpenApiResponse(
                description="Login successful.",
                response={
                    "type": "object",
                    "properties": {
                        "new_complaints": {"type": "integer"},
                        "periods_to_confirm": {"type": "integer"},
                        "new_messages": {"type": "integer"},
                    },
                },
            ),
        },
    )
    @permission_required()
    def get(self, request):
        new_messages_count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        new_complaints_count = 0
        periods_to_confirm_count = None
        if (
            request.user.groups.filter(name="MANAGER").exists()
            or request.user.groups.filter(name="NON_TECHNICAL_EMPLOYEE").exists()
            or request.user.groups.filter(name="ADMIN").exists()
        ):
            new_complaints_count = (
                Complaint.objects.filter(Q(manager=request.user) | Q(manager=None))
                .filter(un_read_user=MessageAuthor.MANAGER)
                .count()
            )
            periods_to_confirm_count = BillingPeriod.objects.filter(
                is_confirmed=False, end_date__lte=django.utils.timezone.now()
            ).count()

            return Response(
                {
                    "new_complaints": new_complaints_count,
                    "new_messages": new_messages_count,
                    "periods_to_confirm": periods_to_confirm_count,
                },
            )
        else:
            new_complaints_count = (
                Complaint.objects.filter(user=request.user)
                .filter(un_read_user=MessageAuthor.USER)
                .count()
            )

        return Response(
            {
                "new_complaints": new_complaints_count,
                "new_messages": new_messages_count,
            },
        )
