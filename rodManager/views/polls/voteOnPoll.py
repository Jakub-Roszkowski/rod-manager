from datetime import datetime

import pytz
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.poll import Option, Poll, Vote
from rodManager.users.validate import permission_required


class AddVoteSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    def create(self, validated_data):
        poll = get_object_or_404(Poll, pk=validated_data["poll_id"])
        if poll.end_date < datetime.now(pytz.utc):
            raise serializers.ValidationError("Pool is closed.")
        option = get_object_or_404(
            Option, option_id=validated_data["option_id"], poll=poll
        )
        user = self.context["request"].user

        vote = Vote.objects.filter(option__poll=poll, user=user).first()
        if vote:
            raise serializers.ValidationError("You have already voted.")
        vote = Vote.objects.create(option=option, user=user)
        return vote


class VoteOnPoll(APIView):
    @extend_schema(
        summary="Vote on poll",
        description="Vote on poll",
        request=AddVoteSerializer,
        responses={
            201: OpenApiResponse(description="Vote added successfully."),
            400: OpenApiResponse(description="Bad request."),
            404: OpenApiResponse(description="Voting not found."),
        },
    )
    @permission_required("rodManager.add_vote")
    def post(self, request):
        serializer = AddVoteSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
