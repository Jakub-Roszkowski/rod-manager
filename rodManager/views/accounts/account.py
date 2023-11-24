from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account


class AccountPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})


class AccountView(APIView):
    @swagger_auto_schema(
        operation_summary="Get a list of accounts",
        manual_parameters=[
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of accounts per page.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Accounts retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "first_name": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "last_name": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                                    "phone": openapi.Schema(type=openapi.TYPE_STRING),
                                    "groups": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(type=openapi.TYPE_STRING),
                                    ),
                                },
                            ),
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
    def get(self, request):
        page_size = request.GET.get("page_size", 10000)
        page_number = request.GET.get("page", 1)

        accounts = Account.objects.all()

        paginator = AccountPagination()
        paginated_accounts = paginator.paginate_queryset(accounts, request)

        serialized_accounts = [
            {
                "id": accounts.id,
                "first_name": accounts.first_name,
                "last_name": accounts.last_name,
                "email": accounts.email,
                "phone": accounts.phone,
                "groups": [group.name for group in accounts.groups.all()],
            }
            for accounts in paginated_accounts
        ]
        return paginator.get_paginated_response(serialized_accounts)
