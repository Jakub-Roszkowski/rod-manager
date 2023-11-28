from django.db.models import Max, Min
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.garden import Garden
from rodManager.dir_models.gardenoffers import GardenOffers


class GardenOfferMinMaxVakuesView(APIView):
    @extend_schema(
        summary="Get garden offers min and max values",
        description="Get garden offers min and max values",
        responses={
            200: OpenApiResponse(
                description="Garden offers min and max values",
                response={
                    "type": "object",
                    "properties": {
                        "min_price": {"type": "number"},
                        "max_price": {"type": "number"},
                        "min_area": {"type": "number"},
                        "max_area": {"type": "number"},
                        "min_predicted_rent": {"type": "number"},
                        "max_predicted_rent": {"type": "number"},
                    },
                },
            )
        },
    )
    def get(self, request):
        min_price = GardenOffers.objects.aggregate(min_price=Min("price"))["min_price"]
        max_price = GardenOffers.objects.aggregate(max_price=Max("price"))["max_price"]
        min_area = Garden.objects.filter(gardenoffers__isnull=False).aggregate(
            min_area=Min("area")
        )["min_area"]
        max_area = Garden.objects.filter(gardenoffers__isnull=False).aggregate(
            max_area=Max("area")
        )["max_area"]
        min_predicted_rent = GardenOffers.objects.aggregate(
            min_predicted_rent=Min("predicted_rent")
        )["min_predicted_rent"]
        max_predicted_rent = GardenOffers.objects.aggregate(
            max_predicted_rent=Max("predicted_rent")
        )["max_predicted_rent"]
        return Response(
            {
                "min_price": min_price,
                "max_price": max_price,
                "min_area": min_area,
                "max_area": max_area,
                "min_predicted_rent": min_predicted_rent,
                "max_predicted_rent": max_predicted_rent,
            },
            status=status.HTTP_200_OK,
        )
