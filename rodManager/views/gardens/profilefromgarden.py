from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rodManager.dir_models.garden import Garden


@swagger_auto_schema(
    methods=["GET"],
    manual_parameters=[
        openapi.Parameter("id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ],
    response=openapi.Response(
        description="Account",
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["GET"])
def profile_from_garden(request):
    if  request.user.is_authenticated:
        if Garden.objects.filter(id=request.data["id"]).exists():
            garden = Garden.objects.get(id=request.data["id"])
            return Response(garden)
        else:
            return Response({"error": "Garden doesn't exist."})
    else:
        return Response({"error": "You don't have permission to view gardens."})
