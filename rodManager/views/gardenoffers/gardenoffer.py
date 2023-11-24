import base64
import os
import uuid

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.db.models import Count, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.gardenoffers import GardenOffers
from rodManager.dir_models.image import Image
from rodManager.users.validate import permission_required


class GardenOfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})


class GardenOfferView(APIView):
    @swagger_auto_schema(
        operation_summary="Get a list of garden offers",
        manual_parameters=[
            openapi.Parameter(
                "price_min",
                openapi.IN_QUERY,
                description="Minimum price.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "price_max",
                openapi.IN_QUERY,
                description="Maximum price.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "area_min",
                openapi.IN_QUERY,
                description="Minimum area.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "area_max",
                openapi.IN_QUERY,
                description="Maximum area.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "predicted_rent_min",
                openapi.IN_QUERY,
                description="Minimum predicted rent.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "predicted_rent_max",
                openapi.IN_QUERY,
                description="Maximum predicted rent.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of offers per page.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Offer retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                                    "body": openapi.Schema(type=openapi.TYPE_STRING),
                                    "contact": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "name": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "phone": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "email": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                        },
                                    ),
                                    "garden_info": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "address": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "area": openapi.Schema(
                                                type=openapi.TYPE_INTEGER
                                            ),
                                            "price": openapi.Schema(
                                                type=openapi.TYPE_NUMBER
                                            ),
                                            "predicted_rent": openapi.Schema(
                                                type=openapi.TYPE_NUMBER
                                            ),
                                        },
                                    ),
                                    "created_at": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format="date-time",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
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
    def get(self, request):
        price_min = request.GET.get("price_min", 0)
        price_max = request.GET.get("price_max", 1e20)
        area_min = request.GET.get("area_min", 0)
        area_max = request.GET.get("area_max", 1e20)
        predicted_rent_min = request.GET.get("predicted_rent_min", 0)
        predicted_rent_max = request.GET.get("predicted_rent_max", 1e20)
        page_size = request.GET.get("page_size", 100000)
        page_number = request.GET.get("page", 1)

        garden_offers = GardenOffers.objects.filter(
            price__gte=price_min,
            price__lte=price_max,
            garden__area__gte=area_min,
            garden__area__lte=area_max,
            predicted_rent__gte=predicted_rent_min,
            predicted_rent__lte=predicted_rent_max,
        )

        paginator = GardenOfferPagination()
        paginated_garden_offers = paginator.paginate_queryset(garden_offers, request)

        serialized_garden_offers = [
            {
                "id": garden_offer.id,
                "title": garden_offer.title,
                "body": garden_offer.body,
                "contact": {
                    "name": garden_offer.contact.first_name,
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

    @swagger_auto_schema(
        operation_summary="Create an announcement",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "body": openapi.Schema(type=openapi.TYPE_STRING),
                "contact_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "garden_info": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "price": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "predicted_rent": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Announcement created successfully.",
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
