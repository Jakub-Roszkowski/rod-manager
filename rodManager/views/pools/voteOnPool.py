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

from rodManager.dir_models.pool import Option, Pool, Vote
from rodManager.users.validate import permission_required


class AddVoteSerializer(serializers.Serializer):
    pool_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    def create(self, validated_data):
        pool = get_object_or_404(Pool, pk=validated_data["pool_id"])
        option = get_object_or_404(
            Option, option_id=validated_data["option_id"], pool=pool
        )
        user = self.context["request"].user

        vote = Vote.objects.filter(option__pool=pool, user=user).first()
        if vote:
            vote.option = option
            vote.save()
        else:
            vote = Vote.objects.create(option=option, user=user)
        return vote


class VoteOnPool(APIView):
    @extend_schema(
        summary="Vote on pool",
        description="Vote on pool",
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
