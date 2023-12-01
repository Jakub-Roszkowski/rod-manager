
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import rodManager.views.payments.userComfirmPaymentsData as userComfirmPaymentsData

from rest_framework import serializers


class PaymentConfirmSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    date = serializers.DateTimeField()


class UserConfirmPaymentsView(APIView):
    @extend_schema(
        summary="Get user confrim payments by ID",
        description="Get user payments based on user ID.",
        parameters=[
            OpenApiParameter(
                name="idUser",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the user.",
            ),
        ],

        responses={
            200: OpenApiResponse(
                description="User payments retrieved successfully.",
                response={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'value': {'type': 'integer'},
                            'date': {'type': 'string', 'format': "date"},
                        }
                    }
                }
            ),
            404: OpenApiResponse(description="User data not found.")
        }
    )
    def get(self, request, idUser):
        try:
            for item in userComfirmPaymentsData.paymentLists:
                if item['idUser'] == idUser:
                    return Response(item['userPaymentList'], status=status.HTTP_200_OK)
            return Response({"message": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Create a new user confirm payment",
        description="Create a new payment confirm entry for a user.",
        request=PaymentConfirmSerializer,
        responses={
            200: OpenApiResponse(description="User data updated successfully."),
            404: OpenApiResponse(description="User data not found."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request, idUser):
        try:
            for item in userComfirmPaymentsData.paymentLists:
                if item['idUser'] == idUser:
                    item['userPaymentList'].append(request.data)
                    # TODO: zmienić stan konta użytkownika
                    # TODO: chyba trzeba tworzyć taką tabele wraz tworzeniem użytkownika
                    return Response({"message": "User data updated successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "User data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
