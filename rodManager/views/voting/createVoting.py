from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.views.voting.votingsData import votings_data as votings


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
        # Trzeba tutaj uważać na date bo podaje razem ze strefą czasową
        # iso_date = request.data['finishDate']
        #
        # date_object = datetime.fromisoformat(iso_date.replace('Z', ''))
        #
        # new_votings = request.data
        # newestvoting = str(date_object)
        # new_votings['finishDate'] = newestvoting

        votings.append(request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)
