from datetime import datetime

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.poll import (
    Option,
    OptionSerializer,
    Poll,
    PollSerializer,
    Vote,
)


class AddOptionSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    label = serializers.CharField()


class AddVotingSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    options = AddOptionSerializer(many=True)
    end_date = serializers.DateTimeField()

    def create(self, validated_data):
        poll = Poll.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            end_date=validated_data["end_date"],
        )
        for option in validated_data["options"]:
            Option.objects.create(
                label=option["label"], option_id=option["option_id"], poll=poll
            )
        return poll


#    def validate(self, data):
#        if data["finish_date"] < datetime.now():
#            raise serializers.ValidationError("Finish date must be in the future")
#        return data


class CreatePoll(APIView):
    @extend_schema(
        summary="Add poll",
        description="Add new poll.",
        request=AddVotingSerializer,
        responses={201: PollSerializer},
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

        serializer = AddVotingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = PollSerializer(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
