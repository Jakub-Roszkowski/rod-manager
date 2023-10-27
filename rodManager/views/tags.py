from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rodManager.dir_models.tag import Tag
from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from rodManager.users.validate import validateUser


class TagView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
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
    def get(self, request):
        tags = Tag.objects.all()
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
    def post(self, request):
        validate = validateUser(request, False, "rodManager.add_tag")
        if validate:
            return validate
        else:
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
