from rest_framework.decorators import api_view
from rest_framework.response import Response
from dir_models.garden import Garden
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    },
)
def garden_list(request):
    gardens = Garden.objects.all()
    garden_list = garden_serializer(gardens, request.user)
    return Response(garden_list)


def garden_serializer(gardens, user):
    perms = user.get_all_permissions()

    garden_list = []
    for garden in gardens:
        if garden.is_public or user.is_authenticated:
            temp = {
                "id": garden.id,
                "sector": garden.sector,
                "avenue": garden.avenue,
                "number": garden.number,
                "area": garden.area,
                "status": garden.status,
            }
            if "rodManager.change_garden" in perms:
                temp["leaseholderID"] = garden.leaseholderID
            garden_list.append(temp)
    return garden_list