from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class FeeSerializer(serializers.Serializer):
    feeID = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    value = serializers.IntegerField()


class FeeListSerializer(serializers.ListSerializer):
    child = FeeSerializer()


class UtilityValuesSerializer(serializers.Serializer):
    electricValue = serializers.IntegerField()
    waterValue = serializers.IntegerField()


class DateSerializer(serializers.Serializer):
    date = serializers.DateTimeField()


class LeaseFeeView(APIView):
    @extend_schema(
        summary="Edit leaseFees data",
        description="Edit leaseFees data",
        request=FeeListSerializer,
        responses={
            200: OpenApiResponse(description="leaseFees data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def patch(self, request):
        try:
            paymentsData.payments["leaseFees"] = request.data

            return Response(
                {"message": "leaseFees data updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UtilityFeeView(APIView):
    @extend_schema(
        summary="Edit UtilityFee data",
        description="Edit UtilityFee data",
        request=FeeListSerializer,
        responses={
            200: OpenApiResponse(description="UtilityFee data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def patch(self, request):
        try:
            paymentsData.payments["utilityFees"] = request.data

            return Response(
                {"message": "UtilityFee data updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdditionalFeeView(APIView):
    @extend_schema(
        summary="Edit AdditionalFee data",
        description="Edit AdditionalFee data",
        request=FeeListSerializer,
        responses={
            200: OpenApiResponse(
                description="AdditionalFee data updated successfully."
            ),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def patch(self, request):
        paymentID = int(request.data["feeID"])
        try:
            for fee in paymentsData.payments["additionalFees"]:
                if fee["feeID"] == paymentID:
                    fee["name"] = request.data["name"]
                    fee["type"] = request.data["type"]
                    fee["value"] = request.data["value"]
                    return Response(
                        {"message": "AdditionalFee data updated successfully"},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"message": "AdditionalFeedata updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Create AdditionalFee",
        description="Create AdditionalFee",
        request=FeeSerializer,
        responses={
            201: OpenApiResponse(description="AdditionalFee created successfully."),
            400: OpenApiResponse(description="Bad request."),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def post(self, request):
        try:
            new_fee_data = {
                "feeID": int(request.data.get("feeID")),
                "name": request.data.get("name"),
                "type": request.data.get("type"),
                "value": int(request.data.get("value")),
            }

            # Dodaj nową opłatę do listy
            paymentsData.payments["additionalFees"].append(new_fee_data)

            return Response(
                {"message": "AdditionalFee created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Delete AdditionalFee",
        description="Delete AdditionalFee by ID",
        parameters=[
            OpenApiParameter(
                name="feeID", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY
            )
        ],
        responses={
            204: OpenApiResponse(description="AdditionalFee deleted successfully."),
            404: OpenApiResponse(description="AdditionalFee not found."),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def delete(self, request):
        feeID = int(request.query_params.get("feeID"))
        try:
            # Znajdź opłatę dodatkową do usunięcia
            for index, fee in enumerate(paymentsData.payments["additionalFees"]):
                if fee["feeID"] == feeID:
                    del paymentsData.payments["additionalFees"][index]
                    return Response(
                        {"message": f"Succes Delate"}, status=status.HTTP_204_NO_CONTENT
                    )

            # Jeśli nie znaleziono opłaty o podanym ID
            return Response(
                {"message": f"No AdditionalFee with ID {feeID} found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UtilityValuesView(APIView):
    @extend_schema(
        summary="Edit utilityValues data",
        description="Edit utilityValues data",
        request=UtilityValuesSerializer,
        responses={
            200: OpenApiResponse(
                description="utilityValues data updated successfully."
            ),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def patch(self, request):
        try:
            paymentsData.payments["utilityValues"] = request.data

            return Response(
                {"message": "utilityValues updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DateView(APIView):
    @extend_schema(
        summary="Edit date data",
        description="Edit date data",
        request=DateSerializer,
        responses={
            200: OpenApiResponse(description="date data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        },
    )
    def patch(self, request):
        try:
            paymentsData.payments["date"] = request.data

            return Response(
                {"message": "date updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
