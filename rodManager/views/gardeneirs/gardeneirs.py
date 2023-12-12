from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class AccountView(APIView):
    @extend_schema(
        summary="Get accounts",
        description="Get all accounts in the system.",
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number.",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page size.",
            ),
            OpenApiParameter(
                name="payment_arrears",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="If true, only return accounts with payment arrears.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Accounts retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone": {"type": "string"},
                                    "groups": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "balance": {"type": "number"},
                                },
                            },
                        },
                    },
                },
            )
        },
    )
    @permission_required("rodManager.view_account")
    def get(self, request):
        accounts = Account.objects.filter(groups__name__contains='GARDENER')
        if request.query_params.get("payment_arrears") == "true":
            accounts = [
                account for account in accounts if account.calculate_balance() < 0
            ]

        paginator = RODPagination()
        paginated_accounts = paginator.paginate_queryset(accounts, request)

        serialized_accounts = [
            {
                "id": accounts.id,
                "first_name": accounts.first_name,
                "last_name": accounts.last_name,
                "email": accounts.email,
                "phone": accounts.phone,
                "groups": [group.name for group in accounts.groups.all()],
                "balance": accounts.calculate_balance(),
            }
            for accounts in paginated_accounts
        ]
        return paginator.get_paginated_response(serialized_accounts)
