from rest_framework.decorators import api_view
from rest_framework.response import Response
from rodManager.dir_models.garden import Garden
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status


@api_view(['GET'])
@swagger_auto_schema(
    responses={
        201: openapi.Response(
            description="Garden list.",
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_OBJECT),
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
def garden_list(request):
    if not request.user.is_authenticated:
        return Response({"error": "You don't have permission to view gardens."}, status=status.HTTP_403_FORBIDDEN)
    gardens = Garden.objects.all()
    
    return Response(serializers.serialize("json", gardens))



@api_view(['get'])
@swagger_auto_schema(
    responses= openapi.Response(
        description="Garden count.",
        type=openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    
)
def garden_count(request):
    if request.user.is_authenticated:
        return Response({"count": Garden.objects.count()})
    else:
        return Response({"error": "You don't have permission to view gardens."})