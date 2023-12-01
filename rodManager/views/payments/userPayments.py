
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

from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    value = serializers.IntegerField()
    date = serializers.DateTimeField()


class UserPaymentsView(APIView):
    @extend_schema(
        summary="Get user payments by ID",
        description="Get user payments based on user ID.",
        parameters=[
            OpenApiParameter(
                name="idUser",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Sector information",
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
                                    "date": {"type": "string", "format": "date"}
                                }
                            }
                        }
                    }
                }
            ),
            404: OpenApiResponse(description="User data not found.")
        }
    )
    def get(self, request, idUser):
        # TODO chyba trzeba będzie tworzyc taką liste przy rejestracji ale nie wiem
        try:
            for item in userPaymentsData.individualPayments:
                if item['userID'] == idUser:
                    return Response(item, status=status.HTTP_200_OK)
            return Response({"message": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Create a new user payment",
        description="Create a new payment entry for a user.",
        request=PaymentSerializer,
        responses={
            200: OpenApiResponse(description="User data updated successfully."),
            404: OpenApiResponse(description="User data not found."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request, idUser):
        try:
            for item in userPaymentsData.individualPayments:
                if item['userID'] == idUser:
                    item['paymentsList'].append(request.data)

                    return Response({"message": "User data updated successfully"}, status=status.HTTP_200_OK)
            #     TODO pamiętać ze trzeba zaktualizować stan konta
            return Response({"message": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
