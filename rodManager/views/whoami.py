from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "You are not logged in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )
