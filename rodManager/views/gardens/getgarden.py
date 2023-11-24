from rest_framework.decorators import api_view
from rest_framework.response import Response
from rodManager.dir_models.garden import Garden
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
@api_view(['GET'])
@swagger_auto_schema(
request_body=openapi.Schema(
    type = openapi.TYPE_OBJECT,
    properties = {
        "index": openapi.Schema(type=openapi.TYPE_INTEGER),
        "size": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=["index", "size"],
),
responses= openapi.Response(
    description="Garden list.",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_OBJECT),
)
)
def garden_in_bulk(request):
    if request.user.is_authenticated:
        gardens = Garden.objects.iterator()[request.GET["index"]:request.GET["index"]+request.GET["size"]]
        return Response(gardens)
    else:
        return Response({"error": "You don't have permission to view gardens."})
                                  
@api_view(['post'])       
@swagger_auto_schema(
    request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=["id"],
    ),
    responses= openapi.Response(
        description="Garden.",
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
)
def garden_by_id(request):
    if request.user.is_authenticated:
        if Garden.objects.filter(id=request.data["id"]).exists():
            garden = Garden.objects.get(id=request.data["id"])
            return Response(garden)
        else:
            return Response({"error": "Garden doesn't exist."})
    else:
        return Response({"error": "You don't have permission to view gardens."})