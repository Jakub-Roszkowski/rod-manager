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
from rodManager.views.payments.edits import FeeListSerializer, FeeSerializer


class ChangeStateSerializer(serializers.Serializer):
    state = serializers.CharField()

    def validate_state(self, value):
        if value in [
            ComplaintStatus.ACCEPTED,
            ComplaintStatus.INPROGRESS,
            ComplaintStatus.COMPLETE,
            ComplaintStatus.REJECTED,
        ]:
            return value
        raise serializers.ValidationError("Wrong state")


class ChangeState(APIView):
    @extend_schema(
        summary="Change complaint state",
        description="Change complaint state, available states: Accepted, InProgress, Complete, Rejected.",
        request=ChangeStateSerializer,
        responses=ComplaintSerializer,
    )
    @permission_required("rodManager.change_complaint")
    def patch(self, request, complaint_id):
        complaints = (
            Complaint.objects.filter(id=complaint_id, manager=request.user)
            .annotate(
                last_update_date=Coalesce(
                    Max("messages__creation_date"), F("open_date")
                )
            )
            .order_by("-last_update_date")
        )
        if complaints.exists():
            complaint = complaints.first()
            serializer = ChangeStateSerializer(data=request.data)
            if serializer.is_valid():
                complaint.state = serializer.validated_data["state"]
                if (
                    complaint.state == ComplaintStatus.COMPLETE
                    or complaint.state == ComplaintStatus.REJECTED
                ):
                    complaint.close_date = timezone.now()
                complaint.save()
                response_serializer = ComplaintSerializer(complaint)
                return Response(response_serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response(status=status.HTTP_404_NOT_FOUND)
