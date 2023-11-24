from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.event import Event


class EventView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of events",
        manual_parameters=[
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="Year of event",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "month",
                openapi.IN_QUERY,
                description="Month of event",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of events",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "date": openapi.Schema(type=openapi.TYPE_STRING),
                        "related_announcement": openapi.Schema(
                            type=openapi.TYPE_INTEGER
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
        year = request.GET.get("year")
        month = request.GET.get("month")
        if year and month:
            events = Event.objects.filter(date__year=year, date__month=month)
        elif year:
            events = Event.objects.filter(date__year=year)
        elif month:
            events = Event.objects.filter(date__month=month)
        else:
            events = Event.objects.all()
        events = sorted(events, key=lambda event: event.date)
        return Response(
            [
                {
                    "id": event.pk,
                    "name": event.name,
                    "date": event.date,
                    "related_announcement": event.announcement.pk,
                }
                for event in events
            ]
        )
