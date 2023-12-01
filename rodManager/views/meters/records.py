
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rodManager.dir_models.record import Record, RecordSerializer
from rodManager.libs.rodpagitation import RODPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse


class RecordsCRUD(ApiView):
    """
    Records CRUD
    """
    model = Record
    serializer_class = RecordSerializer
    pagination_class = RODPagination
    @extend_schema(
    summary="Get records",
    description="Get all records.",
    parameters=[
        OpenApiParameter(name="page", type=OpenApiTypes.INT),
        OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Record list.",
            response=RecordSerializer(many=True),
        ),
    }
    )
    def get(self, request):
        paginator = RODPagination()
        if  request.user.is_authenticated:
            records = paginator.paginate_queryset(Record.objects.all().order_by("id"), request)
            return paginator.get_paginated_response(RecordSerializer(records).data)
        else:
            return Response({"error": "You don't have permission to view records."}, status=status.HTTP_403_FORBIDDEN)

