from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime

from rodManager.views.voting.votingsData import converted_votings as votings


class CurrentsVotings(APIView):
    @swagger_auto_schema(
        operation_summary="Get currents votings",
        responses={
            200: openapi.Response(
                description="Get currents votings",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                        "options": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                  items=openapi.Schema(
                                                      type=openapi.TYPE_OBJECT,
                                                      properties={
                                                          'optionId': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                          'label': openapi.Schema(type=openapi.TYPE_STRING),
                                                      },
                                                  ),
                                                  ),

                        "finishDate": openapi.Schema(type=openapi.TYPE_STRING),
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
        current_votings = votings
        current_date = datetime.now()

        # Filtrujemy głosowania zakończone po obecnym czasie
        filtered_votings = [voting for voting in current_votings if voting.finishDate > current_date]

        try:
            response_data = [
                {
                    "id": voting.id,
                    "title": voting.title,
                    "description": voting.description,
                    "options": [
                        {"optionId": option.optionId, "label": option.label}
                        for option in voting.options
                    ],
                    "finishDate": voting.finishDate.isoformat(),  # Konwersja finishDate na format ISO
                }
                for voting in filtered_votings
            ]

            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
