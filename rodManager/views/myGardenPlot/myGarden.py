from datetime import datetime
from enum import Enum

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.dir_models.fee import Fee, FeeCalculationType, FeeFeeType
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.payment import Payment, PaymentType


class MyGardenAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get garden plot information",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "sector": openapi.Schema(type=openapi.TYPE_STRING),
                        "avenue": openapi.Schema(type=openapi.TYPE_STRING),
                        "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "area": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "leaseholder": openapi.Schema(type=openapi.TYPE_STRING),
                        "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "date": openapi.Schema(type=openapi.FORMAT_DATE),
                        "mediaIndividual": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "mediaConsumption": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                        "leaseFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                        "utilityFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                        "additionalFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                        "individualFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                                },
                            ),
                        ),
                    },
                    required=[
                        "sector",
                        "avenue",
                        "number",
                        "area",
                        "leaseholder",
                        "value",
                        "date",
                    ],
                ),
            ),
            400: openapi.Response(
                description="Invalid request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def get(self, request):
        garden = None
        try:
            garden = Garden.objects.get(leaseholderID=request.user)
        except Garden.DoesNotExist:
            pass
        haveGarden = False

        if garden != None:
            haveGarden = True
        billing_periods = (
            BillingPeriod.objects.filter(is_confirmed=True).order_by("-end_date").all()
        )
        billing_period = None
        billing_period2 = None
        date_from = None
        if len(billing_periods) == 1:
            billing_period = billing_periods[0]
        elif len(billing_periods) > 1:
            billing_period = billing_periods[0]
            billing_period2 = billing_periods[1]
            date_from = billing_period2.confimation_date

        mediaIndividualFees = []
        leaseFees = []
        utilityFees = []
        additionalFees = []
        individualFees = []

        if not date_from:
            payments = Payment.objects.filter(user=request.user).exclude(
                type=PaymentType.BILLPAYMENT
            )
        else:
            payments = Payment.objects.filter(
                user=request.user, date__gte=date_from
            ).exclude(type=PaymentType.BILLPAYMENT)

        for payment in payments:
            if payment.related_fee:
                if (
                    payment.type == PaymentType.PAYMENT
                    or payment.type == PaymentType.INDIVIDUAL
                ):
                    value = payment.related_fee.value
                    sumvalue = payment.amount * -1
                else:
                    value = payment.related_fee.value * -1
                    sumvalue = payment.amount
                type = None
                if payment.related_fee.calculation_type == FeeCalculationType.PERGARDEN:
                    type = FeeCalculationType.PERGARDEN
                elif (
                    payment.related_fee.calculation_type == FeeCalculationType.PERMETER
                ):
                    type = FeeCalculationType.PERMETER
                if payment.related_fee.fee_type == FeeFeeType.LEASE:
                    leaseFees.append(
                        {
                            "name": payment.related_fee.name,
                            "type": type,
                            "value": value,
                            "sum": sumvalue,
                        }
                    )
                elif payment.related_fee.fee_type == FeeFeeType.UTILITY:
                    utilityFees.append(
                        {
                            "name": payment.related_fee.name,
                            "type": type,
                            "value": value,
                            "sum": sumvalue,
                        }
                    )
                elif payment.related_fee.fee_type == FeeFeeType.ADDITIONAL:
                    additionalFees.append(
                        {
                            "name": payment.related_fee.name,
                            "type": type,
                            "value": value,
                            "sum": sumvalue,
                        }
                    )
            else:
                value = payment.amount * -1
                individualFees.append({"name": payment.description, "value": value})

        if mediaIndividualFees:
            mediaIndividualFees.append(
                {
                    "name": "Razem",
                    "mediaConsumption": None,
                    "value": sum([fee["value"] for fee in mediaIndividualFees]),
                }
            )
        else:
            mediaIndividualFees.append(
                {
                    "name": "Razem",
                    "mediaConsumption": None,
                    "value": 0,
                }
            )

        if leaseFees:
            leaseFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": sum([fee["sum"] for fee in leaseFees]),
                }
            )
        else:
            leaseFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": 0,
                }
            )
        if utilityFees:
            utilityFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": sum([fee["sum"] for fee in utilityFees]),
                }
            )
        else:
            utilityFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": 0,
                }
            )
        if additionalFees:
            additionalFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": sum([fee["sum"] for fee in additionalFees]),
                }
            )
        else:
            additionalFees.append(
                {
                    "name": "Razem",
                    "type": None,
                    "value": None,
                    "sum": 0,
                }
            )
        if individualFees:
            individualFees.append(
                {
                    "name": "Razem",
                    "value": sum([fee["value"] for fee in individualFees]),
                }
            )
        else:
            individualFees.append(
                {
                    "name": "Razem",
                    "value": 0,
                }
            )

        balance = request.user.calculate_balance() * -1
        if balance <= 0:
            balance = 0
            billing_period = None

        garden_plot_info = {
            "sector": garden.sector if haveGarden else None,
            "avenue": garden.avenue if haveGarden else None,
            "number": garden.number if haveGarden else None,
            "area": garden.area if haveGarden else None,
            "leaseholder": request.user.first_name + " " + request.user.last_name,
            "value": balance,
            "date": billing_period.payment_date if billing_period else None,
            "mediaIndividual": mediaIndividualFees,
            "leaseFees": leaseFees,
            "utilityFees": utilityFees,
            "additionalFees": additionalFees,
            "individualFees": individualFees,
        }

        return Response(garden_plot_info, status=status.HTTP_200_OK)
