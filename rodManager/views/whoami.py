from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.users.validate import permission_required


class WhoamiView(APIView):
    @extend_schema(
        summary="Who am I",
        description="Get information about the currently logged in user.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                },
            },
            401: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },
        },
    )
    @permission_required()
    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )
