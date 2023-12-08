from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.complaint import (
    Complaint,
    ComplaintSerializer,
    Message,
    MessageAuthor,
    MessageSerializer,
)


class AddMessageSerializer(serializers.Serializer):
    content = serializers.CharField()
    complaint = serializers.PrimaryKeyRelatedField(queryset=Complaint.objects.all())

    def create(self, validated_data):
        complaint = validated_data["complaint"]
        if complaint.user == validated_data["user"]:
            author = MessageAuthor.USER
        else:
            if (
                validated_data["user"].groups.filter(name="MANAGER").exists()
                or validated_data["user"]
                .groups.filter(name="NON_TECHNICAL_EMPLOYEE")
                .exists()
                or validated_data["user"].groups.filter(name="ADMIN").exists()
            ):
                author = MessageAuthor.MANAGER
            else:
                raise serializers.ValidationError(
                    {"error": "Wrong user - not your conversation"}, status=400
                )
        message = Message.objects.create(
            content=validated_data["content"], complaint=complaint, author=author
        )
        return message


class MessageView(APIView):
    @extend_schema(
        summary="Create message",
        description="Create a new message.",
        request=AddMessageSerializer,
        responses=MessageSerializer,
    )
    def post(self, request):
        serializer = AddMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_serializer = MessageSerializer(serializer.instance)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)
