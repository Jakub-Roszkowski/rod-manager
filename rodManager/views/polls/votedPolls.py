from datetime import datetime

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.poll import Option, Poll, PollSerializer, Vote


class VotedPolls(APIView):
    @extend_schema(
        summary="Currents polls",
        description="Get currents polls.",
        responses={200: PollSerializer(many=True)},
    )
    def get(self, request):
        polls = Poll.objects.filter(
            end_date__gte=datetime.now(), options__votes__user=request.user
        )

        serializer = PollSerializer(polls, many=True, context={"request": request})
        return Response(serializer.data)
