from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rodManager.dir_models.garden import Garden


@swagger_auto_schema(
    method="delete",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=["id"],
    ),
    responses={
        200: openapi.Response(
            description="Garden deleted.",
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        403: openapi.Response(
            description="Forbidden.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    },
)
@api_view(["DELETE"])
def delete_garden(request):
    if "rodManager.manageGardens" not in request.user.get_all_permissions():
        return Response(
            {"error": "You don't have permission to delete gardens."},
            status=status.HTTP_403_FORBIDDEN,
        )
    if Garden.objects.filter(id=request.data["id"]).exists():
        Garden.objects.get(id=request.data["id"]).delete()
        return Response(
            {"success": "Garden deleted successfully."}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST
        )
