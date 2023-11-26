from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.views.voting.votingsData import votings_data as votings

class VoteOnVotingAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'voteId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'selectedOptionId': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['voteId', 'selectedOptionId'],
        ),
        responses={
            201: "Vote added successfully",
            400: "Bad Request - Invalid data provided",
            404: "Voting or selected option does not exist"
        },
        operation_summary='Vote on a voting option',
        operation_description='Endpoint to vote on a specific voting option by providing the IDs.'
    )
    def post(self, request):
        try:
            vote_id = request.data.get('voteId')
            selected_option_id = request.data.get('selectedOptionId')

            # TODO: logika i trzeba też zrobić, że jeśli użytkownik już głosował, to może tylko zmienić głos

            for voting in votings:
                if voting['id'] == vote_id:
                    for option in voting['options']:
                        if option['optionId'] == selected_option_id:
                            option['votes'] += 1


            return Response("Vote added successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)