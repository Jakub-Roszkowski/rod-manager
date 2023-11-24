from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.garden import Garden


class AvailableGardensView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of available gardens",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_STRING),
                            "sector": openapi.Schema(type=openapi.TYPE_STRING),
                            "avenue": openapi.Schema(type=openapi.TYPE_STRING),
                            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "area": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "status": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            ),
        }
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
