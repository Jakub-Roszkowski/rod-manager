from datetime import date, timedelta

from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
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


class ConfirmBillingPeriodView(APIView):
    @extend_schema(
        summary="Confirm billing period",
        description="Confirm billing period in the system.",
        responses=BillingPeriodSerializer,
    )
    # @permission_required()
    def post(self, request, billing_period_id):
        if billing_period_id is None:
            return Response(
                {"error": "billing_period_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        billingperiod = get_object_or_404(BillingPeriod, pk=billing_period_id)
        if billingperiod.is_confirmed:
            return Response(
                {"error": "Billing period is already confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # check if previous billing periods is confirmed
        billingperiods = BillingPeriod.objects.filter(
            start_date__lt=billingperiod.start_date
        ).order_by("-start_date")
        if billingperiods.exists():
            if not billingperiods.first().is_confirmed:
                return Response(
                    {"error": "Previous billing period is not confirmed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if billingperiod.payment_date <= date.today():
            return Response(
                {"error": "Payment date must be in the future."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TUTAJ DZIEJE SIĘ CAŁA MAGIA DOPISYWANIA UŻYTKOWNIKOM OPŁAT NA STANY KONT
        billingperiod.is_confirmed = True
        billingperiod.save()
        return Response(BillingPeriodSerializer(billingperiod).data)
