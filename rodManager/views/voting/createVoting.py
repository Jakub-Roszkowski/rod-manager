from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.views.voting.votingsData import converted_votings as votings, convert_to_datetime, Option, VotingTopic


class AddVoting(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'options': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'optionId': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'label': openapi.Schema(type=openapi.TYPE_STRING),
                            'votes': openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
                'finishDate': openapi.Schema(type=openapi.FORMAT_DATETIME),
            },
        ),
        responses={201: 'Created', 400: 'Bad Request'},
        operation_summary='Create a new voting',
        operation_description='Endpoint to create a new voting.',
    )
    def post(self, request):
        try:
            new_voting_data = request.data  # Przyjmujemy dane nowego głosowania z żądania

            # Tutaj możesz dodać walidację danych nowego głosowania, sprawdzenie poprawności pól itp.

            # Tworzymy nową instancję klasy VotingTopic na podstawie danych z żądania
            new_voting = VotingTopic(
                _id=new_voting_data.get("id"),
                title=new_voting_data.get("title"),
                description=new_voting_data.get("description"),
                options=[
                    Option(
                        option_id=option.get("optionId"),
                        label=option.get("label"),
                        votes=option.get("votes", 0)  # Domyślnie 0, można dostosować do własnych potrzeb
                    )
                    for option in new_voting_data.get("options", [])
                ],
                finish_date=convert_to_datetime(new_voting_data.get("finishDate"))
            )

            # Dodaj nowe głosowanie do listy votings_data
            votings.append(new_voting)

            return Response(new_voting_data, status=status.HTTP_201_CREATED)  # Zwracamy nowe głosowanie
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
