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


class FeeSerializer(serializers.ModelSerializer):
    calculated_value = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = ["id", "name", "calculation_type", "value", "calculated_value"]

    def get_calculated_value(self, obj):
        calculated_value = calculate_total_fee(obj)
        return calculated_value


class CurrentFeeView(APIView):
    @extend_schema(
        summary="Get current fees",
        description="Get current fees in the system.",
        responses=FeeSerializer(many=True),
        examples=[
            OpenApiExample(
                "Example response",
                value={
                    "billing_period": 1,
                    "start_date": "2022-01-01",
                    "end_date": "2022-01-31",
                    "payment_date": "2022-02-01",
                    "is_confirmed": False,
                    "lease_fees": [
                        {"id": 1, "name": "Lease Fee 1", "calculated_value": 1234.0}
                    ],
                    "utility_fees": [
                        {"id": 2, "name": "Utility Fee 1", "calculated_value": 1234.0}
                    ],
                    "additional_fees": [
                        {
                            "id": 3,
                            "name": "Additional Fee 1",
                            "calculated_value": 1234.0,
                        }
                    ],
                },
                summary="A typical response",
            )
        ],
    )
    @permission_required()
    def get(self, request):
        billing_period = (
            BillingPeriod.objects.filter(is_confirmed=False)
            .order_by("start_date")
            .first()
        )
        leaseFees = []
        utilityFees = []
        additionalFees = []
        if billing_period:
            leaseFees = Fee.objects.filter(
                fee_type="Lease", billing_period=billing_period.id
            )
            utilityFees = Fee.objects.filter(
                fee_type="Utility", billing_period=billing_period.id
            )
            additionalFees = Fee.objects.filter(
                fee_type="Additional", billing_period=billing_period.id
            )

        data = {
            "lease_fees": FeeSerializer(leaseFees, many=True).data,
            "utility_fees": FeeSerializer(utilityFees, many=True).data,
            "additional_fees": FeeSerializer(additionalFees, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
