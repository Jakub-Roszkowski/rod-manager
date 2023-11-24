from django.db.models import Max, Min
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.garden import Garden
from rodManager.dir_models.gardenoffers import GardenOffers


class GardenOfferMinMaxVakuesView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Garden offers min and max values",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "min_price": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "max_price": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "min_area": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "max_area": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "min_predicted_rent": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "max_predicted_rent": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            )
        }
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
