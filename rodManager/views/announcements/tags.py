from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.tag import Tag
from rodManager.users.validate import permission_required


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()


class TagView(APIView):
    @extend_schema(
        summary="Get tags",
        description="Get all tags in the system.",
        responses={
            200: OpenApiResponse(
                description="Tags retrieved successfully.",
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "times_used": {"type": "integer"},
                        },
                    },
                },
            ),
        },
    )
    def get(self, request):
        tags = Tag.objects.all()
        tags = sorted(tags, key=lambda tag: tag.times_used, reverse=True)
        return Response(
            [{"name": tag.name, "times_used": tag.times_used} for tag in tags]
        )

    @extend_schema(
        summary="Add tag",
        description="Add tag to the system.",
        request=TagSerializer,
        responses={
            201: OpenApiResponse(
                description="Tag added successfully.",
            ),
            400: OpenApiResponse(
                description="Tag already exists.",
            ),
        },
    )
    @permission_required("rodManager.add_tag")
    def post(self, request):
        if request.data.get("name"):
            name = request.data["name"]
            if Tag.objects.filter(name=name).exists():
                tag = Tag.objects.get(name=name)
                tag.times_used += 1
                tag.save()
                return Response(status=status.HTTP_201_CREATED)
            tag = Tag(name=name, times_used=0)
            tag.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
