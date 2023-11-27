import base64
import uuid

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.db.models import Count, Q
from drf_spectacular import openapi
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.announcement import Announcement
from rodManager.dir_models.event import Event
from rodManager.dir_models.image import Image
from rodManager.dir_models.tag import Tag
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class EventSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    name = serializers.CharField()


class AnnouncmentSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    event = EventSerializer()


class AnnouncementView(APIView):
    @extend_schema(
        summary="Get announcements",
        description="Get all announcements in the system.",
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number.",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page size.",
            ),
            OpenApiParameter(
                name="tags",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by tags.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Announcements retrieved successfully.",
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
                                    "tags": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "date": {
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                    "event": {
                                        "type": "object",
                                        "properties": {
                                            "date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "name": {"type": "string"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            )
        },
    )
    def get(self, request):
        tags = request.GET.get("tags", "").split(",")
        page_size = request.GET.get("page_size", 10000)
        page_number = request.GET.get("page", 1)
        if tags == [""]:
            announcements = Announcement.objects.all()
        else:
            announcements = Announcement.objects.filter(tags__name__in=tags)
        annotations = {"num_tags": Count("tags", filter=Q(tags__name__in=tags))}
        announcements = announcements.annotate(**annotations)

        announcements = announcements.order_by("-num_tags", "-date")

        paginator = RODPagination()
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

        for announcement in serialized_announcements:
            event = Event.objects.filter(announcement_id=announcement["id"]).first()
            if event:
                event_object = {"date": event.date, "name": event.name}
                announcement["event"] = event_object

        return paginator.get_paginated_response(serialized_announcements)

    @extend_schema(
        summary="Create an announcement",
        request=AnnouncmentSerializer,
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
    @permission_required("rodManager.add_announcement")
    def post(self, request):
        if request.data.get("title"):
            title = request.data["title"]
            announcement = Announcement(title=title)
            announcement.save()
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
            if (
                request.data.get("event")
                and request.data["event"].get("date")
                and request.data["event"].get("name")
            ):
                event = Event(
                    announcement=announcement,
                    date=request.data["event"]["date"],
                    name=request.data["event"]["name"],
                )
                event.save()

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
