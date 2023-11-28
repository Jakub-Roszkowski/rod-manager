
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rodManager.dir_models.garden import Garden, PlotStatus
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status




@swagger_auto_schema(
    method="post",
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
@api_view(['POST'])
def create_garden(request):
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
        