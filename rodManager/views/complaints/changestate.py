from django.db import models
from django.db.models import F, Max
from django.db.models.functions import Coalesce
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.complaint import (
    Complaint,
    ComplaintSerializer,
    ComplaintStatus,
)
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class ChangeStateSerializer(serializers.Serializer):
    state = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.REPORTED,
    )


class ChangeState(APIView):
    @extend_schema(
        summary="Change complaint state",
        description="Change complaint state",
        parameters=[
            OpenApiParameter(
                name="complaint_id",
                type=OpenApiTypes.INT,
                description="Complaint id",
            )
        ],
        request=ChangeStateSerializer,
        responses=ComplaintSerializer,
    )
    @permission_required("rodManager.change_complaint")
    def patch(self, request, complaint_id):
        complaints = (
            Complaint.objects.filter(id=complaint_id)
            .annotate(
                last_update_date=Coalesce(
                    Max("messages__creation_date"), F("open_date")
                )
            )
            .order_by("-last_update_date")
        )
        if complaints.exists():
            complaint = complaints.first()
            complaint.state = request.data["state"]
            complaint.close_date = timezone.now()
            complaint.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
