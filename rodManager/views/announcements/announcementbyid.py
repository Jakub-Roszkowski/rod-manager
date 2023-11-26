from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   OpenApiTypes, extend_schema)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.announcement import Announcement


class AnnouncementByIdView(APIView):
    @extend_schema(
        summary="Get announcement by id",
        description="Get announcement by id",
        responses={
            200: OpenApiResponse(
                description="Announcement retrieved successfully.",
                response={
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
                            "format": "date",
                        },
                        "event": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "format": "date",
                                },
                                "name": {"type": "string"},
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
    def get(self, request, announcement_id):
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            response_data = {
                "id": announcement.id,
                "title": announcement.title,
                "body": announcement.body,
                "tags": [tag.name for tag in announcement.tags.all()],
                "date": announcement.date,
            }
            if hasattr(announcement, "event") and announcement.event:
                response_data["event"] = {
                    "date": announcement.event.date,
                    "name": announcement.event.name,
                }
            return Response(response_data)
        except Announcement.DoesNotExist:
            return Response({"error": "Announcement does not exist."}, status=400)
