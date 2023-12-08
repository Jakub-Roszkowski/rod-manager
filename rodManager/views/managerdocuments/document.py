from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.managerdocument import ManagerDocument


class ManagerDocumentPostSerializer(serializers.Serializer):
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ManagerDocument.objects.filter(file=""),
        allow_null=True,
        required=False,
    )
    file = serializers.FileField(allow_null=True, required=False)

    def create(self, validated_data):
        return ManagerDocument.create_document(**validated_data)


class ManagerDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ManagerDocument.objects.all(), allow_null=True
    )
    file = serializers.FileField(allow_null=True, required=False)


class ManagerDocumentView(APIView):
    @extend_schema(
        summary="Get manager documents",
        description='Dostarczone dokumenty będą w poniższym formacje. Jeśli dokument jest folderem i posiada wewnątrz pliki, to w polu `items` będą zawarte dokumenty w nim zawarte. Jeśli dokument jest plikiem, to w polu `file_url` będzie zawarty link do pliku. \nPrzykład: \n```json\n[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/managerdocuments/plik.txt"\n    }]\n}]\n``` \n\n\nJeżeli folder jest pusty może zostać przekonwertowany na plik przez przesłanie pliku.\nW folderze może istnieć inny folder, struktura może być dowolnie zagnieżdżona.\nPrzykład zagnieżdżenia: \n```json\n[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/managerdocuments/plik.txt"\n    }, {\n        "id": 3,\n        "name": "folder2",\n        "items": [{\n            "id": 4,\n            "name": "plik2",\n            "file_url": "/mediafiles/managerdocuments/plik2.txt"\n        }]\n    }]\n}]\n```',
    )
    def get(self, request):
        root_documents = ManagerDocument.objects.filter(parent__isnull=True)
        data = [doc.to_dict() for doc in root_documents]
        print(data)
        return Response(data)

    @extend_schema(
        summary="Create manager document",
        description="Create a new manager document.",
        request=ManagerDocumentPostSerializer,
        responses={201: ManagerDocumentSerializer},
    )
    def post(self, request):
        serializer = ManagerDocumentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resultSerializer = ManagerDocumentSerializer(serializer.instance)
        return Response(resultSerializer.data, status=status.HTTP_201_CREATED)
