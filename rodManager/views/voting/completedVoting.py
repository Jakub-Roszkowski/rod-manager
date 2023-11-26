from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from rodManager.views.voting.votingsData import votings_data as votings


class CompletedVotings(APIView):
    @swagger_auto_schema(
        operation_summary="Get completed votings",
        responses={
            200: openapi.Response(
                description="Get completed votings",
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
                                                          'votes': openapi.Schema(type=openapi.TYPE_INTEGER),
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

        # Obecna data
        current_date = datetime.now()

        # Filtrujemy głosowania z datą zakończenia większą niż obecna data
        filtered_votings = [voting for voting in votings if
                            datetime.fromisoformat(voting["finishDate"]) < current_date]

        try:
            response_data = filtered_votings
            return Response(response_data)
        except Exception as e:
            return Response({"error": "Votings  do not exist."}, status=400)