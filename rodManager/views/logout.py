from django.contrib.auth import logout
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Logout",
        description="Logout the currently logged in user.",
        responses={
            200: OpenApiResponse(description="Logout successful"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
