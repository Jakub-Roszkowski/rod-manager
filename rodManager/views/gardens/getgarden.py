from django.core import serializers
from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rodManager.dir_models.garden import Garden


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("page_size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    response=openapi.Response(
        description="Garden list.",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT),
    ),
)
@api_view(["GET"])
def garden_in_bulk(request):
    if "rodManager.manageGardens" not in request.user.get_all_permissions():
        index = int(request.GET["page"]) - 1
        size = int(request.GET["page_size"])
        paginator = Paginator(Garden.objects.all().order_by("id"), size)
        gardens = paginator.get_page(index)
        return Response(
            serializers.serialize("json", gardens), status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "You don't have permission to view gardens."},
            status=status.HTTP_403_FORBIDDEN,
        )


@swagger_auto_schema(
    methods=["GET"],
    manual_parameters=[
        openapi.Parameter("id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response(
            description="Garden.",
            schema=openapi.Schema(
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
        ),
    },
)
@api_view(["GET"])
def garden_by_id(request):
    if request.user.is_authenticated:
        if Garden.objects.filter(id=request.data["id"]).exists():
            garden = Garden.objects.get(
                id=request.GET["id"],
            )
            return Response(garden, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Garden doesn't exist."}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"error": "You don't have permission to view gardens."},
            status=status.HTTP_403_FORBIDDEN,
        )
