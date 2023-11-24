from django.db.models import Max, Min
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.gardenoffers import GardenOffers


class ContactView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Managers contact information",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "phone": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        }
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
