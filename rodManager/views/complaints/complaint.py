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


class AddComplaintSerializer(serializers.Serializer):
    title = serializers.CharField()

    def create(self, validated_data):
        user = validated_data["user"]
        complaint = Complaint.objects.create(title=validated_data["title"], user=user)
        return complaint


class ComplaintView(APIView):
    pagination_class = RODPagination

    @extend_schema(
        summary="Get complaints",
        description="Get all complaints in the system.",
        parameters=[
            OpenApiParameter(name="page", type=OpenApiTypes.INT),
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
        ],
        responses=ComplaintSerializer(many=True),
    )
    @permission_required()
    def get(self, request):
        # print first complaint
        if (
            request.user.groups.filter(name="MANAGER").exists()
            or request.user.groups.filter(name="NON_TECHNICAL_EMPLOYEE").exists()
            or request.user.groups.filter(name="ADMIN").exists()
        ):
            complaints = (
                Complaint.objects.all()
                .annotate(
                    last_update_date=Coalesce(
                        Max("messages__creation_date"), F("open_date")
                    )
                )
                .order_by("-last_update_date")
            )
        else:
            complaints = (
                Complaint.objects.filter(user=request.user)
                .annotate(
                    last_update_date=Coalesce(
                        Max("messages__creation_date"), F("open_date")
                    )
                )
                .order_by(F("-last_update_date"))
            )
        serializer = ComplaintSerializer(complaints, many=True)
        paginator = RODPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(page)

    @extend_schema(
        summary="Create complaint",
        description="Create a new complaint.",
        request=AddComplaintSerializer,
        responses=ComplaintSerializer,
    )
    @permission_required()
    def post(self, request):
        serializer = AddComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_serializer = ComplaintSerializer(serializer.instance)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)
