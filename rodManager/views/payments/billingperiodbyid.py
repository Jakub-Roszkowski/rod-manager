from datetime import date, timedelta

from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class BillingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPeriod
        fields = "__all__"


class AddBillingPeriodSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = BillingPeriod
        fields = ["payment_date"]

    def update(self, instance, validated_data):
        if validated_data.get("payment_date") < instance.end_date:
            raise serializers.ValidationError(
                {"error": "Payment date must be greater than end date."}
            )
        if validated_data.get("payment_date") <= date.today():
            raise serializers.ValidationError(
                {"error": "Payment date must be in the future."}
            )
        payment_date = validated_data.get("payment_date")
        if payment_date is None:
            payment_date = validated_data["end_date"] + timedelta(days=31)
        instance.payment_date = payment_date
        instance.save()
        return instance


class BillingPeriodByIdView(APIView):
    @extend_schema(
        summary="Change billing period payment date",
        description="Change billing period payment date in the system.",
        request=AddBillingPeriodSerializer,
        responses=BillingPeriodSerializer,
    )
    # @permission_required()
    def patch(self, request, billing_period_id):
        billingperiod = BillingPeriod.objects.get(pk=billing_period_id)
        serializer = AddBillingPeriodSerializer(
            billingperiod, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
