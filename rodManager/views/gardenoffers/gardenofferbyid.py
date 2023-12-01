from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.gardenoffers import GardenOffers


class GardenInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    predicted_rent = serializers.IntegerField()


class GardenOfferSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    contact_id = serializers.IntegerField()
    garden_info = GardenInfoSerializer()


class GardenOfferByIdView(APIView):
    @extend_schema(
        summary="Get an announcement",
        description="Get an announcement",
        responses={
            200: OpenApiResponse(
                description="Announcement retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "body": {"type": "string"},
                        "contact_id": {"type": "integer"},
                        "garden_info": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "price": {"type": "integer"},
                                "predicted_rent": {"type": "integer"},
                            },
                        },
                    },
                },
            ),
            400: OpenApiResponse(
                description="Announcement does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                    },
                },
            ),
        },
    )
    def get(self, request, id=None):
        if id:
            if GardenOffers.objects.filter(id=id).exists():
                gardenoffer = GardenOffers.objects.get(id=id)
                response_data = {
                    "id": gardenoffer.id,
                    "title": gardenoffer.title,
                    "body": gardenoffer.body,
                    "contact_id": gardenoffer.contact.id,
                    "garden_info": {
                        "id": gardenoffer.garden.id,
                        "price": gardenoffer.price,
                        "predicted_rent": gardenoffer.predicted_rent,
                    },
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Announcement does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Announcement ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        summary="Delete an announcement",
        description="Delete an announcement",
        responses={
            200: OpenApiResponse(
                description="Announcement deleted successfully.",
                response={
                    "type": "object",
                    "properties": {"success": {"type": "string"}},
                },
            ),
            400: OpenApiResponse(
                description="Bad request.",
                response={
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
            ),
        },
    )
    def delete(self, request, id=None):
        if id:
            if GardenOffers.objects.filter(id=id).exists():
                gardenoffer = GardenOffers.objects.get(id=id)
                gardenoffer.delete()
                return Response(
                    {"success": "Announcement deleted successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Announcement does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Announcement ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
