
from telnetlib import GA
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response

from rodManager.dir_models.garden import Garden, GardenSerializer, PlotStatus
from django.core import serializers
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rodManager.libs.rodpagitation import RODPagination
import drf_spectacular.serializers as drfserializers




class GardensCRUD(APIView):  
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    pagination_class = RODPagination
    @extend_schema(
    summary="Get gardens",
    description="Get all gardens.",
    parameters=[
        OpenApiParameter(name="page", type=OpenApiTypes.INT),
        OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Garden list.",
            response=GardenSerializer(many=True),
        ),
    }
    
    )
    def get(self, request):
        paginator = RODPagination()
        if  request.user.is_authenticated:
            gardens = paginator.paginate_queryset(Garden.objects.all().order_by("id"), request)
            return paginator.get_paginated_response(GardenSerializer(gardens).data)
        else:
            return Response({"error": "You don't have permission to view gardens."}, status=status.HTTP_403_FORBIDDEN)
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "sector": openapi.Schema(type=openapi.TYPE_STRING),
            "avenue": openapi.Schema(type=openapi.TYPE_STRING),
            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
            "area": openapi.Schema(type=openapi.TYPE_INTEGER),
            "status": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["sector", "avenue", "number", "area", "status"],
    ),
    responses={
        201: openapi.Response(
            description="Garden created.",
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    },
)
    def post(self, request):
        if request.user.is_authenticated:
            if not request.data.get("sector") or not request.data.get("avenue") or not request.data.get("number") or not request.data.get("area") or not request.data.get("status"):
                return Response({"error": "Sector, avenue, number, area and status are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.data["status"] not in [PlotStatus.AVAILABLE, PlotStatus.UNAVAILABLE]:
                return Response({"error": "Status must be dostępna or niedostępna."}, status=status.HTTP_400_BAD_REQUEST)
            
            if Garden.objects.filter(
                sector=request.data["sector"],
                avenue=request.data["avenue"],
                number=request.data["number"],
            ).exists():
                return Response({"error": "Garden already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            newgarden = Garden.objects.create(
                sector=request.data["sector"],
                avenue=request.data["avenue"],
                number=request.data["number"],
                area=request.data["area"],
                status=request.data["status"],
            )
            newgarden.save()
            return Response({"success": "Garden created successfully."}, status=status.HTTP_201_CREATED)
        else :
            return Response({"error": "You don't have permission to create gardens."}, status=status.HTTP_403_FORBIDDEN)
        
    
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "sector": openapi.Schema(type=openapi.TYPE_STRING),
            "avenue": openapi.Schema(type=openapi.TYPE_STRING),
            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
            "area": openapi.Schema(type=openapi.TYPE_INTEGER),
            "status": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["id", "sector", "avenue", "number", "area", "status"],
    ),
    responses={
        200: openapi.Response(
            description="Garden edited.",
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        403: openapi.Response(
            description="Forbidden.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    }
)
    def put(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You don't have permission to edit gardens."}, status=status.HTTP_403_FORBIDDEN)
        if not request.data["id"]:
                return Response({"error": "Garden ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data["sector"] or not request.data["avenue"] or not request.data["number"] or not request.data["area"] or not request.data["status"]:
                return Response({"error": "Sector, avenue, number, area and status are required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["status"] not in ["dostępna", "niedostępna"]:
            return Response({"error": "Status must be dostępna or niedostępna."}, status=status.HTTP_400_BAD_REQUEST)
        if not Garden.objects.filter(
            id = request.data["id"],
            sector=request.data["sector"],
            avenue=request.data["avenue"],
            number=request.data["number"],
        ).exists():
            return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        garden = Garden.objects.get(id=request.data["id"])
        garden.leaseholderID = request.data["leaseholderID"]
        garden.status = request.data["status"]
        garden.save()
        return Response({"success": "Garden edited successfully."}, status=status.HTTP_200_OK)  
        
    @swagger_auto_schema(
  request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=["id"],
    ),
    responses={
        200: openapi.Response(
            description="Garden deleted.",
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        403: openapi.Response(
            description="Forbidden.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    },
    )
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You don't have permission to delete gardens."}, status=status.HTTP_403_FORBIDDEN)
        if Garden.objects.filter(id=request.data["id"]).exists():
            Garden.objects.get(id=request.data["id"]).delete()
            return Response({"success": "Garden deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)