import base64
import uuid

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.gardenoffers import GardenOffers
from rodManager.dir_models.image import Image
from rodManager.libs.rodpagitation import RODPagination


class GardenInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    predicted_rent = serializers.IntegerField()


class GardenOfferSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    contact_id = serializers.IntegerField()
    garden_info = GardenInfoSerializer()


class GardenOfferView(APIView):
    @extend_schema(
        summary="Get a list of garden offers",
        description="Get a list of garden offers in the system.",
        parameters=[
            OpenApiParameter(
                name="sort_by",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Sort by.",
                enum=["created_at", "area", "price", "predicted_rent"],
            ),
            OpenApiParameter(
                name="sort_order",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Sort order.",
                enum=["asc", "desc"],
            ),
            OpenApiParameter(
                name="price_min",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Minimum price.",
            ),
            OpenApiParameter(
                name="price_max",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Maximum price.",
            ),
            OpenApiParameter(
                name="area_min",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Minimum area.",
            ),
            OpenApiParameter(
                name="area_max",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Maximum area.",
            ),
            OpenApiParameter(
                name="predicted_rent_min",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Minimum predicted rent.",
            ),
            OpenApiParameter(
                name="predicted_rent_max",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Maximum predicted rent.",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Number of offers per page.",
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Offer retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "title": {"type": "string"},
                                    "body": {"type": "string"},
                                    "contact": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "phone": {"type": "string"},
                                            "email": {"type": "string"},
                                        },
                                    },
                                    "garden_info": {
                                        "type": "object",
                                        "properties": {
                                            "address": {"type": "string"},
                                            "area": {"type": "integer"},
                                            "price": {"type": "number"},
                                            "predicted_rent": {"type": "number"},
                                        },
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                },
                            },
                        },
                    },
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
    def get(self, request):
        price_min = request.GET.get("price_min", 0)
        price_max = request.GET.get("price_max", 1e20)
        area_min = request.GET.get("area_min", 0)
        area_max = request.GET.get("area_max", 1e20)
        predicted_rent_min = request.GET.get("predicted_rent_min", 0)
        predicted_rent_max = request.GET.get("predicted_rent_max", 1e20)
        page_size = request.GET.get("page_size", 100000)
        page_number = request.GET.get("page", 1)
        sort_by = request.GET.get("sort_by", "created_at")
        sort_order = request.GET.get("sort_order", "desc")

        if sort_by not in ["created_at", "area", "price", "predicted_rent"]:
            return Response(
                {
                    "error": "Invalid sort_by parameter. (created_at, area, price, predicted_rent)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if sort_order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid sort_order parameter. (asc, desc)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        garden_offers = GardenOffers.objects.filter(
            price__gte=price_min,
            price__lte=price_max,
            garden__area__gte=area_min,
            garden__area__lte=area_max,
            predicted_rent__gte=predicted_rent_min,
            predicted_rent__lte=predicted_rent_max,
        )

        if sort_order == "desc":
            garden_offers = garden_offers.order_by(f"-{sort_by}")
        else:
            garden_offers = garden_offers.order_by(sort_by)

        paginator = RODPagination()
        paginated_garden_offers = paginator.paginate_queryset(garden_offers, request)

        serialized_garden_offers = [
            {
                "id": garden_offer.id,
                "title": garden_offer.title,
                "body": garden_offer.body,
                "contact": {
                    "name": garden_offer.contact.first_name
                    + " "
                    + garden_offer.contact.last_name,
                    "phone": garden_offer.contact.phone,
                    "email": garden_offer.contact.email,
                },
                "garden_info": {
                    "address": str(garden_offer.garden.sector)
                    + ","
                    + str(garden_offer.garden.avenue)
                    + ","
                    + str(garden_offer.garden.number),
                    "area": garden_offer.garden.area,
                    "price": garden_offer.price,
                    "predicted_rent": garden_offer.predicted_rent,
                },
                "created_at": garden_offer.created_at,
            }
            for garden_offer in paginated_garden_offers
        ]

        return paginator.get_paginated_response(serialized_garden_offers)

    @extend_schema(
        summary="Create an announcement",
        description="Create an announcement",
        request=GardenOfferSerializer,
        responses={
            201: OpenApiResponse(
                description="Announcement created successfully.",
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
    def post(self, request):
        if request.data.get("title"):
            title = request.data["title"]
            contact_id = request.data.get("contact_id")
            garden_id = request.data.get("garden_info").get("id")
            price = request.data.get("garden_info").get("price")
            predicted_rent = request.data.get("garden_info").get("predicted_rent")

            if contact_id and garden_id and price and predicted_rent:
                contact = Account.objects.filter(id=contact_id)
                garden = Garden.objects.filter(id=garden_id)
                if not contact.exists():
                    return Response(
                        {"error": "Contact does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not garden.exists():
                    return Response(
                        {"error": "Garden does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                print(garden.first().status)
                if garden.first().status != "dostepna":
                    return Response(
                        {"error": "Garden is not available."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if GardenOffers.objects.filter(garden=garden.first()).exists():
                    return Response(
                        {"error": "Garden already has an offer."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                print("nie podano wszystkich wymaganych pól")
                print(contact_id, garden_id, price, predicted_rent)
                return Response(
                    {
                        "error": "Contact, garden, price and predicted_rent fields are required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            gardenoffer = GardenOffers(title=title)

            if request.data.get("body"):
                soup = BeautifulSoup(request.data.get("body"), "html.parser")
                img_tags = soup.find_all("img")
                image_formats = {
                    "jpeg": "jpg",
                    "png": "png",
                    "gif": "gif",
                    "webp": "webp",
                    "bmp": "bmp",
                    "vnd.microsoft.icon": "ico",
                    "tiff": "tiff",
                }
                for img_tag in img_tags:
                    src = img_tag["src"]
                    for format_prefix, extension in image_formats.items():
                        if src.startswith(f"data:image/{format_prefix};base64,"):
                            base64_data = src[
                                len(f"data:image/{format_prefix};base64,") :
                            ]

                            filename = f"{uuid.uuid4()}.{extension}"
                            image_data = base64.b64decode(base64_data)
                            image_model_instance = Image(name=filename, file=filename)
                            image_model_instance.file.save(
                                filename, ContentFile(image_data), save=True
                            )

                            img_tag["src"] = f"/api/protectedfile/images/{filename}"
                            break

                updated_html_code = str(soup)
                gardenoffer.body = updated_html_code

            gardenoffer.contact = contact.first()
            gardenoffer.garden = garden.first()
            gardenoffer.price = price
            gardenoffer.predicted_rent = predicted_rent

            gardenoffer.save()
            return Response(
                {"success": "Announcement created successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Title field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
