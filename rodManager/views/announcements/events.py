from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.event import Event


class EventView(APIView):
    @extend_schema(
        summary="Get events",
        description="Get all events in the system.",
        parameters=[
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by year.",
            ),
            OpenApiParameter(
                name="month",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by month.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Events retrieved successfully.",
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "date": {"type": "string", "format": "date"},
                            "related_announcement": {"type": "integer"},
                        },
                    },
                },
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
