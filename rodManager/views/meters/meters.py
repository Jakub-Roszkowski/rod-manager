




from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rodManager.libs import RODPagination
from rodManager.dir_models.meter import Meter, MeterSerializer


class MetersCRUD(APIView):

    queryset = Meter.objects.all()
    serializer_class = MeterSerializer
    pagination_class = RODPagination

    @extend_schema(
    summary="Get meters",
    description="Get all meters.",
    parameters=[
        OpenApiParameter(name="page", type=OpenApiTypes.INT),
        OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Meter list.",
            response=MeterSerializer(many=True),
        ),
    }
    
    )
    def get(self, request):
        paginator = RODPagination()
        if  request.user.is_authenticated:
            meters = paginator.paginate_queryset(Meter.objects.all().order_by("id"), request)
            return paginator.get_paginated_response(MeterSerializer(meters).data)
        else:
            return Response({"error": "You don't have permission to view meters."}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
    summary="Create meter",
    request=MeterSerializer,
    responses={
        201: OpenApiResponse(
            description="Meter created."
        ),
        400: OpenApiResponse(
            description="Bad request."
        ),
        403: OpenApiResponse(
            description="Forbidden."
        ),
    }
    )
    def post(self, request):
        if request.user.is_authenticated:
            if not request.data.get("serial") or not request.data.get("status"):
                return Response({"error": "Serial and status are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if Meter.objects.filter(serial=request.data["serial"]).exists():
                return Response({"error": "Meter already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            newmeter = Meter.objects.create(
                serial=request.data["serial"],
                status=request.data["status"],
            )
            newmeter.save()
            return Response({"message": "Meter created."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You don't have permission to create meters."}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
    summary="Update meter",
    request=MeterSerializer,
    responses={
        200: OpenApiResponse(
            description="Meter updated."
        ),
        400: OpenApiResponse(
            description="Bad request."
        ),
        403: OpenApiResponse(
            description="Forbidden."
        ),
    }
    )
    def put(self, request):
        if request.user.is_authenticated:
            try:
                meter = Meter.objects.get(pk=pk)
            except Meter.DoesNotExist:
                return Response({"error": "Meter does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.data.get("serial"):
                meter.serial = request.data["serial"]
            if request.data.get("status"):
                meter.status = request.data["status"]
            meter.save()
            return Response({"message": "Meter updated."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You don't have permission to update meters."}, status=status.HTTP_403_FORBIDDEN)