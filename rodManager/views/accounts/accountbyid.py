
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account


class AccountByIdView(APIView):
    @swagger_auto_schema(
        operation_summary="Get account by id",
        responses={
            200: openapi.Response(
                description="Accounts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "phone": openapi.Schema(type=openapi.TYPE_STRING),
                        "groups": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                        ),
                    },
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
    def get(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            response_data = {
                "id": account.id,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email,
                "phone": account.phone,
                "groups": [group.name for group in account.groups.all()],
            }

            return Response(response_data)
        except Announcement.DoesNotExist:
            return Response({"error": "Account does not exist."}, status=400)
