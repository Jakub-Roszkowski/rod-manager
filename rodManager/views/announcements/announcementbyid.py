
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.announcement import Announcement


# add get for getting announcement by id
class AnnouncementByIdView(APIView):
    @swagger_auto_schema(
        operation_summary="Get announcement by id",
        responses={
            200: openapi.Response(
                description="Announcement",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "body": openapi.Schema(type=openapi.TYPE_STRING),
                        "tags": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                        ),
                        "date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date-time",
                        ),
                        "event": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "date": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format="date-time",
                                ),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                            },
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
