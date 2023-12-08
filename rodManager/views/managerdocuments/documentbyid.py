from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.managerdocument import ManagerDocument


class UpdateManagerDocumentSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False, required=False)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ManagerDocument.objects.filter(file=""),
        allow_null=True,
        required=False,
    )
    file = serializers.FileField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.parent = validated_data.get("parent", instance.parent)
        if validated_data.get("file", None):
            if instance.file:
                instance.file.delete()
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance


class ManagerDocumentByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ManagerDocument.objects.all(), allow_null=True
    )
    file = serializers.FileField(allow_null=True, required=False)


class ManagerDocumentByIdView(APIView):
    @extend_schema(
        summary="Get manager document",
        description="Get manager document by id.",
        request=UpdateManagerDocumentSerializer,
        responses={200: ManagerDocumentByIdSerializer},
    )
    def put(self, request, document_id):
        document = ManagerDocument.objects.get(pk=document_id)
        serializer = UpdateManagerDocumentSerializer(document, data=request.data)
        serializer.is_valid(raise_exception=True)
        response = ManagerDocumentByIdSerializer(serializer.save()).data
        return Response(response)

    @extend_schema(
        summary="Delete manager document",
        description="Delete manager document by id.",
        responses={204: None},
    )
    def delete(self, request, document_id):
        document = ManagerDocument.objects.get(pk=document_id)
        if document.file:
            document.file.delete()
        document.delete()
        return Response(status=204)
