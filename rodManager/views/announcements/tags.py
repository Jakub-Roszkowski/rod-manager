from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.tag import Tag
from rodManager.users.validate import permission_required


class TagView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="List of tags.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "times_used": openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                ),
            ),
            400: openapi.Response(
                description="Bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def get(self, request):
        tags = Tag.objects.all()
        tags = sorted(tags, key=lambda tag: tag.times_used, reverse=True)
        return Response(
            [{"name": tag.name, "times_used": tag.times_used} for tag in tags]
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["name"],
        ),
        responses={
            201: openapi.Response(
                description="Tag created successfully.",
            ),
            400: openapi.Response(
                description="Bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
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
