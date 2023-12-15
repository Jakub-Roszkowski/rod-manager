import threading
from datetime import date, datetime, timedelta

from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.dir_models.fee import Fee, FeeCalculationType, FeeFeeType
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.meter import Meter
from rodManager.dir_models.notification import NotificationType
from rodManager.dir_models.payment import Payment, PaymentType
from rodManager.libs.addnotification import add_notification
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


def addpayment(amount, user, description, type, related_fee=None, date=date.today()):
    payment = Payment.objects.create(
        user=user,
        type=type,
        date=date,
        amount=amount,
        description=description,
        related_fee=related_fee,
    )

    payment.save()

    return payment


def add_payments_and_notifications(billingperiod, previous_billingperiod, user):
    previous_billingperiod_confirmation_date = None
    if previous_billingperiod is not None:
        previous_billingperiod_confirmation_date = (
            previous_billingperiod.confirmation_date
        )

    fees = Fee.objects.filter(billing_period=billingperiod)

    gardens = Garden.objects.exclude(leaseholderID__isnull=True)

    rod_meters = Meter.objects.exclude(garden__in=gardens)

    rod_meters_water_sum = 0

    rod_meters_electricity_sum = 0

    for meter in rod_meters:
        if meter.type == "woda":
            rod_meters_water_sum += meter.calculate_usage(
                billingperiod.confirmation_date,
                previous_billingperiod_confirmation_date,
            )

        elif meter.type == "prąd":
            rod_meters_electricity_sum += meter.calculate_usage(
                billingperiod.confirmation_date,
                previous_billingperiod_confirmation_date,
            )

    gardens_meters_sum = 0

    gardens_sum = 0

    for garden in gardens:
        gardens_meters_sum += garden.area

        gardens_sum += 1

    for garden in gardens:
        for fee in fees:
            if fee.fee_type == FeeFeeType.UTILITY:
                if fee.calculation_type == FeeCalculationType.PERGARDEN:
                    if gardens_sum != 0:
                        if fee.name == "Woda":
                            value = rod_meters_water_sum / gardens_sum * fee.value
                            if value > 0:
                                addpayment(
                                    round(value, 2) * -1,
                                    garden.leaseholderID,
                                    'Wspólna opłata: "' + fee.name + '"',
                                    PaymentType.PAYMENT,
                                    related_fee=fee,
                                )

                            my_meter = Meter.objects.filter(garden=garden, type="woda")

                            if my_meter.exists():
                                value = my_meter[0].calculate_usage(
                                    billingperiod.confirmation_date,
                                    previous_billingperiod_confirmation_date,
                                )

                                if value is not None and value > 0:
                                    addpayment(
                                        round(value, 2) * fee.value * -1,
                                        garden.leaseholderID,
                                        'Indywidualna opłata: "' + fee.name + '"',
                                        PaymentType.PAYMENT,
                                        related_fee=fee,
                                    )

                        elif fee.name == "Prąd":
                            value = rod_meters_electricity_sum / gardens_sum * fee.value

                            if value > 0:
                                addpayment(
                                    round(value, 2) * -1,
                                    garden.leaseholderID,
                                    'Wspólna opłata: "' + fee.name + '"',
                                    PaymentType.PAYMENT,
                                    related_fee=fee,
                                )

                            my_meter = Meter.objects.filter(garden=garden, type="prąd")

                            if my_meter.exists():
                                value = my_meter[0].calculate_usage(
                                    billingperiod.confirmation_date,
                                    previous_billingperiod_confirmation_date,
                                )

                                if value is not None and value > 0:
                                    addpayment(
                                        round(value, 2) * fee.value * -1,
                                        garden.leaseholderID,
                                        'Indywidualna opłata: "' + fee.name + '"',
                                        PaymentType.PAYMENT,
                                        related_fee=fee,
                                    )

                elif fee.calculation_type == FeeCalculationType.PERMETER:
                    if gardens_meters_sum != 0:
                        if fee.name == "Woda":
                            value = (
                                rod_meters_water_sum
                                * garden.area
                                / gardens_meters_sum
                                * fee.value
                            )

                            if value > 0:
                                addpayment(
                                    round(value, 2) * -1,
                                    garden.leaseholderID,
                                    'Wspólna opłata: "' + fee.name + '"',
                                    PaymentType.PAYMENT,
                                    related_fee=fee,
                                )

                            my_meter = Meter.objects.filter(garden=garden, type="woda")

                            if my_meter.exists():
                                value = my_meter[0].calculate_usage(
                                    billingperiod.confirmation_date,
                                    previous_billingperiod_confirmation_date,
                                )

                                if value is not None and value > 0:
                                    addpayment(
                                        value * fee.value * -1,
                                        garden.leaseholderID,
                                        'Indywidualna opłata: "' + fee.name + '"',
                                        PaymentType.PAYMENT,
                                        related_fee=fee,
                                    )

                        elif fee.name == "Prąd":
                            value = (
                                rod_meters_electricity_sum
                                * garden.area
                                / gardens_meters_sum
                                * fee.value
                            )

                            if value > 0:
                                addpayment(
                                    round(value, 2) * -1,
                                    garden.leaseholderID,
                                    'Wspólna opłata: "' + fee.name + '"',
                                    PaymentType.PAYMENT,
                                    related_fee=fee,
                                )

                            my_meter = Meter.objects.filter(garden=garden, type="prąd")

                            if my_meter.exists():
                                value = my_meter[0].calculate_usage(
                                    billingperiod.confirmation_date,
                                    previous_billingperiod_confirmation_date,
                                )

                                if value is not None and value > 0:
                                    addpayment(
                                        round(value, 2) * fee.value * -1,
                                        garden.leaseholderID,
                                        'Indywidualna opłata: "' + fee.name + '"',
                                        PaymentType.PAYMENT,
                                        related_fee=fee,
                                    )

            else:
                if fee.calculation_type == FeeCalculationType.PERGARDEN:
                    addpayment(
                        fee.value * -1,
                        garden.leaseholderID,
                        'Opłata: "' + fee.name + '"',
                        PaymentType.PAYMENT,
                        related_fee=fee,
                    )

                elif fee.calculation_type == FeeCalculationType.PERMETER:
                    addpayment(
                        fee.value * garden.area * -1,
                        garden.leaseholderID,
                        'Opłata: "' + fee.name + '"',
                        PaymentType.PAYMENT,
                        related_fee=fee,
                    )

        add_notification(
            garden.leaseholderID,
            NotificationType.INFO,
            "Rozpoczął się nowy okres rozliczeniowy. Prosimy o wpłatę należności.",
            send_email=True,
        )

    add_notification(
        user,
        NotificationType.INFO,
        "Zakończono potwierdzanie okresu rozliczeniowego.",
        send_email=True,
    )


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

        billingperiod.is_confirmed = True

        billingperiod.confirmation_date = timezone.now()

        billingperiod.save()

        try:
            previous_billingperiod = BillingPeriod.objects.filter(
                start_date__lt=billingperiod.start_date
            ).order_by("-start_date")[0]

        except:
            previous_billingperiod = None

        thread = threading.Thread(
            target=add_payments_and_notifications,
            args=(billingperiod, previous_billingperiod, request.user),
        )

        thread.start()

        return Response(BillingPeriodSerializer(billingperiod).data)
