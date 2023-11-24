from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rodManager.dir_models.meter import Meter


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "type": openapi.Schema(type=openapi.TYPE_STRING),
            "adress": openapi.Schema(type=openapi.TYPE_STRING),
            "garden": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=["id", "type"],
    ),
    responses={
        201: openapi.Response(
            description="Record added.",
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
@api_view(["POST"])
def add_record(request):
    if "rodManager.manageRecords" in request.user.get_all_permissions():
        if not request.data["id"] or not request.data["type"]:
            return Response(
                {"error": "ID and type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.data["adress"] and not request.data["garden"]:
            return Response(
                {"error": "Adress or garden are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Meter.objects.filter(id=request.data["id"]).exists():
            return Response(
                {"error": "Meter already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        newmeter = Meter.objects.create(
            id=request.data["id"],
            type=request.data["type"],
            adress=request.data["adress"],
            garden=request.data["garden"],
        )
        newmeter.save()
        return Response(
            {"success": "Meter added successfully"}, status=status.HTTP_201_CREATED
        )
