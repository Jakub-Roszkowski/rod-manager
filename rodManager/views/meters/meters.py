





from itertools import chain
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rodManager.libs.rodpagitation import RODPagination 
from rodManager.dir_models.meter import Meter, MeterLastRecordSerializer
from rodManager.dir_models.record import Record, RecordSerializer
from rodManager.dir_models.garden import Garden
import datetime


class MetersCRUD(APIView):

    queryset = Meter.objects.all()
    serializer_class = MeterLastRecordSerializer
    pagination_class = RODPagination

    @extend_schema(
    summary="Get meters",
    description="Get all meters.",
    parameters=[
        OpenApiParameter(name="page", type=OpenApiTypes.INT),
        OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
        OpenApiParameter(name="type", type=OpenApiTypes.STR),
    ],
    responses={
        200: OpenApiResponse(
            description="Meter list.",
            response=MeterLastRecordSerializer(many=True),
        ),
    }
    
    )
    def get(self, request):
        paginator = RODPagination()
        
        if  request.user.is_authenticated:
            if request.GET.get("type"):
                no_garden_meters = Meter.objects.filter(type=request.GET["type"], garden = None).order_by("adress")
                meters = Meter.objects.filter(type=request.GET["type"]).exclude(garden = None).order_by("adress")
                meters = paginator.paginate_queryset(meters, request)
                no_garden_meters = paginator.paginate_queryset(no_garden_meters, request)
                return paginator.get_paginated_response(list(chain(MeterLastRecordSerializer(meters,many=True).data, MeterLastRecordSerializer(no_garden_meters,many=True).data)))
            else:
                no_garden_meters = Meter.objects.filter( garden = None).order_by("adress")
                meters = Meter.objects.filter().exclude(garden = None).order_by("adress")
                meters = paginator.paginate_queryset(meters, request)
                no_garden_meters = paginator.paginate_queryset(no_garden_meters, request)
                return paginator.get_paginated_response(list(chain(MeterLastRecordSerializer(meters,many=True).data, MeterLastRecordSerializer(no_garden_meters,many=True).data)))
            
        else:
            return Response({"error": "You don't have permission to view meters."}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
    summary="Create meter",
    request=MeterLastRecordSerializer,
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
            if not request.data.get("serial") or not request.data.get("type"):
                return Response({"error": "Serial and type are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if Meter.objects.filter(serial=request.data["serial"]).exists():
                return Response({"error": "Meter already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            newmeter = Meter.objects.create(
                serial=request.data["serial"],
                type=request.data["type"],
            )
            if request.data.get("adress"):
                newmeter.adress = request.data["adress"]
            if request.data.get("garden"):
                if not Garden.objects.filter(id=request.data["garden"]).exists():
                    return Response({"error": "Garden does not exist."}, status=status.HTTP_400_BAD_REQUEST)
                newmeter.garden = Garden.objects.get(id=request.data["garden"])
            if request.data.get("value"):
                Record.objects.create(
                    meter=newmeter,
                    value=request.data["value"],
                    date = datetime.date.today(),
                    time = datetime.datetime.now().time()
                )
            newmeter.save()
            return Response({"message": "Meter created."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You don't have permission to create meters."}, status=status.HTTP_403_FORBIDDEN)
    
    
    @extend_schema(
    summary="Delete meter",
    parameters=[
        OpenApiParameter(name="id", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Meter deleted."
        ),
        400: OpenApiResponse(
            description="Bad request."
        ),
        403: OpenApiResponse(
            description="Forbidden."
        ),
    }
    )
    def delete(self, request):
        if request.user.is_authenticated:
            if not request.data.get("serial"):
                return Response({"error": "Serial is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not Meter.objects.filter(serial=request.data["serial"]).exists():
                return Response({"error": "Meter does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            Meter.objects.get(serial=request.data["serial"]).delete()
            return Response({"message": "Meter deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You don't have permission to delete meters."}, status=status.HTTP_403_FORBIDDEN)
        

