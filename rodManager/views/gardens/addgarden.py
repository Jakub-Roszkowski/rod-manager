
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dir_models.garden import Garden
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['POST'])
@swagger_auto_schema(
    responses={
        201: openapi.Response(
            description="Garden created.",
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "sector": openapi.Schema(type=openapi.TYPE_STRING),
                "avenue": openapi.Schema(type=openapi.TYPE_STRING),
                "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                "area": openapi.Schema(type=openapi.TYPE_INTEGER),
                "status": openapi.Schema(type=openapi.TYPE_STRING),
            },
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
def create_garden(request):
    if "rodManager.createGarden" in request.user.get_all_permissions():
        newgarden = Garden.objects.create(
            sector=request.data["sector"],
            avenue=request.data["avenue"],
            number=request.data["number"],
            area=request.data["area"],
            status=request.data["status"],
        )
        newgarden.save()
        