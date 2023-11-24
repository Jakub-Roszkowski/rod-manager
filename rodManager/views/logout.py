from django.contrib.auth import logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=None,
        responses={
            status.HTTP_200_OK: openapi.Response("Logout successful"),
        },
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
