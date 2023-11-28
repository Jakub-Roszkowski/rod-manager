from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account


class ContactView(APIView):
    @extend_schema(
        summary="Get managers",
        description="Get all managers in the system.",
        responses={
            200: OpenApiResponse(
                description="Managers retrieved successfully.",
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "phone": {"type": "string"},
                            "email": {"type": "string"},
                        },
                    },
                },
            ),
        },
    )
    def get(self, request):
        managers = Account.objects.filter(groups__name="MANAGER")
        return Response(
            [
                {
                    "id": manager.id,
                    "name": manager.first_name + " " + manager.last_name,
                    "phone": manager.phone,
                    "email": manager.email,
                }
                for manager in managers
            ],
            status=status.HTTP_200_OK,
        )
