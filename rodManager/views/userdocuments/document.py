from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.userdocument import UserDocument


class UserDocumentPostSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=UserDocument.objects.filter(file=""),
        allow_null=True,
        required=False,
    )
    file = serializers.FileField(allow_null=True, required=False)

    def create(self, validated_data):
        if validated_data.get("parent", None):
            if validated_data["parent"].user != validated_data["user"]:
                raise serializers.ValidationError(
                    "Parent document must be owned by user."
                )
        return UserDocument.create_document(**validated_data)


class UserDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=UserDocument.objects.all(), allow_null=True
    )
    file = serializers.FileField(allow_null=True, required=False)


class UserDocumentView(APIView):
    @extend_schema(
        summary="Get user documents",
        description='Dostarczone dokumenty będą w poniższym formacje. Jeśli dokument jest folderem i posiada wewnątrz pliki, to w polu `items` będą zawarte dokumenty w nim zawarte. Jeśli dokument jest plikiem, to w polu `file_url` będzie zawarty link do pliku. \nPrzykład: \n```json\n[{\n"user": 1,\n"documents":[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/userdocuments/plik.txt"\n    }]\n  }]\n}\n{\n"user": 2,\n"documents":[{\n    "id": 3,\n    "name": "folder2",\n    "items": [{\n        "id": 4,\n        "name": "plik2",\n        "file_url": "/mediafiles/userdocuments/plik2.txt"\n    }]\n  }]\n}]\n``` \n\n\nJeżeli folder jest pusty może zostać przekonwertowany na plik przez przesłanie pliku.\nW folderze może istnieć inny folder, struktura może być dowolnie zagnieżdżona.\nPrzykład zagnieżdżenia: \n```json\n...\n[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/userdocuments/plik.txt"\n    }, {\n        "id": 3,\n        "name": "folder2",\n        "items": [{\n            "id": 4,\n            "name": "plik2",\n            "file_url": "/mediafiles/userdocuments/plik2.txt"\n        }]\n    }]\n}]\n...\n```',
    )
    def get(self, request):
        result = []
        for user in Account.objects.all():
            root_documents = UserDocument.objects.filter(parent__isnull=True, user=user)
            data = [doc.to_dict() for doc in root_documents]
            result.append({"user": user.id, "documents": data})
        return Response(result)

    @extend_schema(
        summary="Create user document",
        description="Create a new user document.",
        request=UserDocumentPostSerializer,
        responses={201: UserDocumentSerializer},
    )
    def post(self, request):
        serializer = UserDocumentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resultSerializer = UserDocumentSerializer(serializer.instance)
        return Response(resultSerializer.data, status=status.HTTP_201_CREATED)
