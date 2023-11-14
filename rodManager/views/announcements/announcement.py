from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rodManager.dir_models.tag import Tag
from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from rodManager.users.validate import permission_required
from rodManager.dir_models.announcement import Announcement
from django.core.files.base import ContentFile
from rodManager.dir_models.image import Image
from rodManager.dir_models.tag import Tag
from bs4 import BeautifulSoup
import base64
import os
import uuid
from django.db.models import Count, Q
from rest_framework.pagination import PageNumberPagination


class AnnouncementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AnnouncementView(APIView):
    @swagger_auto_schema(
        operation_summary="Get a list of announcements",
        manual_parameters=[
            openapi.Parameter(
                "tags",
                openapi.IN_QUERY,
                description="Tags to filter by.",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of announcements per page.",
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
                description="Announcements retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "body": openapi.Schema(type=openapi.TYPE_STRING),
                            "tags": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING),
                            ),
                            "date": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
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
        tags = request.GET.getlist("tags", [])
        print(tags)
        new_tags = []
        for tag in tags:
            new_tags.append(tag)

        print(new_tags)
        page_size = request.GET.get("page_size", 10000)
        page_number = request.GET.get("page", 1)

        if tags == []:
            announcements = Announcement.objects.all()
        else:
            announcements = Announcement.objects.filter(tags__name__in=tags)

        annotations = {"num_tags": Count("tags", filter=Q(tags__name__in=tags))}
        announcements = announcements.annotate(**annotations)

        announcements = announcements.order_by("-num_tags", "-date")

        paginator = AnnouncementPagination()
        paginated_announcements = paginator.paginate_queryset(announcements, request)

        serialized_announcements = [
            {
                "id": announcement.id,
                "title": announcement.title,
                "body": announcement.body,
                "tags": [tag.name for tag in announcement.tags.all()],
                "date": announcement.date,
            }
            for announcement in paginated_announcements
        ]

        return paginator.get_paginated_response(serialized_announcements)

    @swagger_auto_schema(
        operation_summary="Create an announcement",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "body": openapi.Schema(type=openapi.TYPE_STRING),
                "tags": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
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
            announcement = Announcement(title=title)
            announcement.save()
            if request.data.get("body"):
                soup = BeautifulSoup(request.data.get("body"), "html.parser")
                img_tags = soup.find_all("img")
                for img_tag in img_tags:
                    src = img_tag["src"]

                    if src.startswith("data:image/jpeg;base64,"):
                        base64_data = src[len("data:image/jpeg;base64,") :]

                        filename = "{}.jpg".format(uuid.uuid4())
                        image_data = base64.b64decode(base64_data)
                        image_model_instance = Image(name=filename, file=filename)
                        image_model_instance.file.save(
                            filename, ContentFile(image_data), save=True
                        )

                        img_tag["src"] = "/api/protectedfile/images/{}".format(filename)

                    elif src.startswith("data:image/png;base64,"):
                        base64_data = src[len("data:image/png;base64,") :]
                        filename = "{}.png".format(uuid.uuid4())

                        image_data = base64.b64decode(base64_data)
                        image_model_instance = Image(name=filename, file=filename)
                        image_model_instance.file.save(
                            filename, ContentFile(image_data), save=True
                        )

                        img_tag["src"] = "/api/protectedfile/images/{}".format(filename)

                updated_html_code = str(soup)
                print(updated_html_code)
                announcement.body = updated_html_code
            if request.data.get("tags"):
                print(request.data["tags"])
                if type(request.data["tags"]) is not list:
                    return Response(
                        {"error": "Tags must be a list."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                for tag in request.data["tags"]:
                    print(tag)
                    if Tag.objects.filter(name=tag).exists():
                        tag = Tag.objects.get(name=tag)
                        tag.times_used += 1
                        tag.save()
                    else:
                        tag = Tag(name=tag, times_used=1)
                        tag.save()

                    announcement.tags.add(tag)

            announcement.save()
            return Response(
                {"success": "Announcement created successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Title field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
