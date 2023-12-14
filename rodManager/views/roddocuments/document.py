from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.roddocument import RodDocument


class RodDocumentPostSerializer(serializers.Serializer):
    name = serializers.CharField()
    file = serializers.FileField()

    def create(self, validated_data):
        if RodDocument.objects.filter(name=validated_data["name"]).exists():
            document = RodDocument.objects.get(name=validated_data["name"])
            document.file.delete()
            document.file = validated_data["file"]
            document.save()
            return document
        return RodDocument.create_document(**validated_data)


class RodDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    file = serializers.SerializerMethodField("get_file")

    def get_file(self, obj):
        if obj.file:
            return "/" + obj.file.name
        return None


class RodDocumentView(APIView):
    @extend_schema(
        summary="Get system documents",
        description="Get system documents.",
        responses=RodDocumentSerializer(many=True),
    )
    def get(self, request):
        documents = RodDocument.objects.all()
        serializer = RodDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create system document",
        description="Create a new system document or overvrite existing.",
        request=RodDocumentPostSerializer,
        responses={201: RodDocumentSerializer},
    )
    def post(self, request):
        serializer = RodDocumentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resultSerializer = RodDocumentSerializer(serializer.instance)
        return Response(resultSerializer.data, status=status.HTTP_201_CREATED)
