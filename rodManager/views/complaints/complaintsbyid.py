from django.db.models import F, Max
from django.db.models.functions import Coalesce
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.complaint import Complaint, ComplaintSerializer
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class ComplaintsById(APIView):
    @extend_schema(
        summary="Get complaints by id",
        description="Get complaints in the system by id.",
        responses=ComplaintSerializer,
    )
    @permission_required()
    def get(self, request, complaint_id):
        if (
            request.user.groups.filter(name="MANAGER").exists()
            or request.user.groups.filter(name="NON_TECHNICAL_EMPLOYEE").exists()
            or request.user.groups.filter(name="ADMIN").exists()
        ):
            complaints = (
                Complaint.objects.filter(id=complaint_id)
                .annotate(
                    last_update_date=Coalesce(
                        Max("messages__creation_date"), F("open_date")
                    )
                )
                .order_by("-last_update_date")
            )
        else:
            complaints = (
                Complaint.objects.filter(user=request.user, id=complaint_id)
                .annotate(
                    last_update_date=Coalesce(
                        Max("messages__creation_date"), F("open_date")
                    )
                )
                .order_by("-last_update_date")
            )
        if complaints.exists():
            complaint = complaints.first()
            serializer = ComplaintSerializer(complaint)
            return Response(serializer.data, status=200)
