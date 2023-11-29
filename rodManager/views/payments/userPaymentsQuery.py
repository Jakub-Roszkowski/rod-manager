from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import rodManager.views.payments.userPaymentsData as userPaymentsData


class UserPaymentsQueryView(APIView):
    @extend_schema(
        summary="Get user payments by Address",
        description="Get user payments based on GardenPlot Leaseholder.",
        parameters=[
            OpenApiParameter(
                name="sector",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Sector information",
            ),
            OpenApiParameter(
                name="avenue",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Avenue information",
            ),
            OpenApiParameter(
                name="number",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Plot number",
            ),
        ],

        responses={
            200: OpenApiResponse(
                description="User payments retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "userID": {"type": "integer"},
                        "paymentsList": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "paymentID": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "value": {"type": "integer"},
                                    "date": {"type": "string", "format": "date-time"}
                                }
                            }
                        }
                    }
                }
            ),
            404: OpenApiResponse(description="User data not found.")
        }
    )
    def get(self, request):
        # TODO ogolnie no trzeba znaleźć dzierżawce takiej działki i zwrócić jego płatności i chyba trzeba będzie tworzyc taką liste przy rejestracji ale nie wiem
        try:
            for item in userPaymentsData.individualPayments:
                if item['userID'] == 1:
                    return Response(item, status=status.HTTP_200_OK)
            return Response({"message": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Delete a user payment",
        description="Delete a payment entry for a user.",
        parameters=[
            OpenApiParameter(
                name='userID',
                type=OpenApiTypes.INT,
                description='ID of the user',
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(

                name='paymentID',
                type=OpenApiTypes.INT,
                description='ID of the payment to delete',
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: OpenApiResponse(description="User payment deleted successfully."),
            404: OpenApiResponse(description="User or payment data not found."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def delete(self, request):
        userID = int(request.query_params.get('userID'))
        paymentID = int(request.query_params.get('paymentID'))

        # TODO: zmienić stan konta użytkownika
        try:
            found_user = False
            found_payment = False

            for item in userPaymentsData.individualPayments:
                if item['userID'] == userID:
                    found_user = True
                    for payment in item['paymentsList']:
                        if payment['paymentID'] == paymentID:
                            found_payment = True
                            item['paymentsList'].remove(payment)
                            return Response({"message": "User payment deleted successfully"},
                                            status=status.HTTP_200_OK)

            if not found_user:
                return Response({"message": f"User with ID {userID} not found"},
                                status=status.HTTP_404_NOT_FOUND)
            elif not found_payment:
                return Response({"message": f"Payment with ID {paymentID} not found for the user {userID}"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
