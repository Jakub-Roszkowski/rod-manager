
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import rodManager.views.payments.paymentsData as paymentsData

from rest_framework import serializers


class PaymentConfirmSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    date = serializers.DateTimeField()


class PaymentsView(APIView):
    @extend_schema(
        summary="Get payments of the ROD",
        description="Get payments of the ROD",
        parameters=[],

        responses={
            200: OpenApiResponse(
                description="User payments retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "format": "date"},
                        "leaseFees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "feeID": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["Za metr", "Za działkę"]
                                    },
                                    "value": {"type": "integer"},
                                }
                            }
                        },
                        "utilityFees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "feeID": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["Za metr", "Za działkę"]
                                    },
                                    "value": {"type": "integer"},
                                }
                            }
                        },
                        "additionalFees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "feeID": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["Za metr", "Za działkę"]
                                    },
                                    "value": {"type": "integer"},
                                }
                            }
                        }
                        ,
                        "UtilityValues": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "electricValue": {"type": "integer"},
                                    "waterValue": {"type": "integer"},
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
        try:
            return Response(paymentsData.payments, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="w opisie jest co to robi",
        description="ogolnie to tu sie potwierdza wszytsko i wtedy idzie informacja dla wszystkich działkowiczów jest rozliczenie itd można zakomentowac jakas funckcje do wysyłanie meili a no i nie wiem jaka tu metoda no i jeszcze robi magie na licznikach",
        request=PaymentConfirmSerializer,
    )
    def put(self, request):
        try:
            return Response({
                "message": "No jest wszystko w porządku,jest dobrze,dobrze robią,dobrze wszystko jest w porządku.Jest git pozdrawiam całą Legnice,dobrych chłopaków i niech sie to trzyma.Dobry przekaz leci"},
                status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
