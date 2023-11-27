from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.garden import Garden


class AvailableGardensView(APIView):
    @extend_schema(
        summary="Get available gardens",
        description="Get all available gardens in the system.",
        responses={
            200: OpenApiResponse(
                description="Gardens retrieved successfully.",
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "sector": {"type": "string"},
                            "avenue": {"type": "string"},
                            "number": {"type": "integer"},
                            "area": {"type": "number"},
                            "status": {"type": "string"},
                        },
                    },
                },
            ),
        },
    )
    def get(self, request):
        gardens = Garden.objects.filter(status="dostepna")

        return Response(
            [
                {
                    "id": garden.id,
                    "sector": garden.sector,
                    "avenue": garden.avenue,
                    "number": garden.number,
                    "area": garden.area,
                    "status": garden.status,
                }
                for garden in gardens
            ],
            status=status.HTTP_200_OK,
        )
