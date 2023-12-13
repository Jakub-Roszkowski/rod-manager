
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rodManager.dir_models.record import Record, RecordSerializer, RecordsValuesSerializer
from rodManager.libs.rodpagitation import RODPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse


class RecordsCRUD(APIView):
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

    @extend_schema(
    summary="Create record",
    request=RecordsValuesSerializer,
    responses={
        200: OpenApiResponse(
            description="Record created.",
            response=RecordSerializer,
        ),
    }
    )
    def post(self, request):
        if  request.user.is_authenticated:
            serializer = RecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You don't have permission to create records."}, status=status.HTTP_403_FORBIDDEN)
        
    @extend_schema(

    summary="Delete record",
    description="Delete record by id.",
    parameters=[
        OpenApiParameter(name="serial", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Record deleted.",
        ),
    }
    )
    def delete(self, request, id):
        if  request.user.is_authenticated:
            try:
                record = Record.objects.get(id=id)
                record.delete()
                return Response(status=status.HTTP_200_OK)
            except Record.DoesNotExist:
                return Response({"error": "Record not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "You don't have permission to delete records."}, status=status.HTTP_403_FORBIDDEN)
        
    
