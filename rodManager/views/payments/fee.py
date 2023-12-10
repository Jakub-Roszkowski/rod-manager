from django.db import models
from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.dir_models.fee import Fee
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


def calculate_total_fee(fee):
    if fee.calculation_type == "PerGarden":
        return fee.value * 10
    elif fee.calculation_type == "PerMeter":
        return fee.value * 100
    else:
        return 0.0


class AddFeeSerializer(serializers.ModelSerializer):
    billing_period = serializers.PrimaryKeyRelatedField(
        queryset=BillingPeriod.objects.all()
    )
    fee_type = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    calculation_type = serializers.CharField(required=True)
    value = serializers.FloatField(required=True)

    class Meta:
        model = Fee
        fields = [
            "billing_period",
            "fee_type",
            "name",
            "calculation_type",
            "value",
        ]

    def create(self, validated_data):
        if validated_data["billing_period"].is_confirmed:
            raise serializers.ValidationError({"error": "Billing period is closed."})
        fee = Fee.objects.create(
            billing_period=validated_data["billing_period"],
            fee_type=validated_data["fee_type"],
            name=validated_data["name"],
            calculation_type=validated_data["calculation_type"],
            value=validated_data["value"],
        )
        fee.save()
        return fee


class FeeSerializer(serializers.ModelSerializer):
    calculated_value = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = ["id", "name", "calculation_type", "value", "calculated_value"]

    def get_calculated_value(self, obj):
        calculated_value = calculate_total_fee(obj)
        return calculated_value


class FeeView(APIView):
    @extend_schema(
        summary="Add fee",
        description="Add fee in the system.",
        request=AddFeeSerializer,
        responses=FeeSerializer(),
    )
    @permission_required()
    def post(self, request):
        serializer = AddFeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
