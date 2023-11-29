
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import rodManager.views.payments.paymentsData as paymentsData

from rest_framework import serializers


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
        }
    )
    def patch(self, request):
        try:
            paymentsData.payments['leaseFees'] = request.data

            return Response({"message": "leaseFees data updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UtilityFeeView(APIView):
    @extend_schema(
        summary="Edit UtilityFee data",
        description="Edit UtilityFee data",
        request=FeeListSerializer,
        responses={
            200: OpenApiResponse(description="UtilityFee data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request):
        try:
            paymentsData.payments['utilityFees'] = request.data

            return Response({"message": "UtilityFee data updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdditionalFeeView(APIView):
    @extend_schema(
        summary="Edit AdditionalFee data",
        description="Edit AdditionalFee data",
        request=FeeListSerializer,
        responses={
            200: OpenApiResponse(description="AdditionalFee data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request):
        try:
            paymentsData.payments['additionalFees'] = request.data

            return Response({"message": "AdditionalFeedata updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UtilityValuesView(APIView):
    @extend_schema(
        summary="Edit utilityValues data",
        description="Edit utilityValues data",
        request=UtilityValuesSerializer,
        responses={
            200: OpenApiResponse(description="utilityValues data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request):
        try:
            paymentsData.payments['utilityValues'] = request.data

            return Response({"message": "utilityValues updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DateView(APIView):
    @extend_schema(
        summary="Edit date data",
        description="Edit date data",
        request=DateSerializer,
        responses={
            200: OpenApiResponse(description="date data updated successfully."),
            500: OpenApiResponse(description="Server error occurred."),
        }
    )
    def patch(self, request):
        try:
            paymentsData.payments['date'] = request.data

            return Response({"message": "date updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
