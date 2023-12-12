import django.utils.timezone
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

from rodManager.dir_models.account import Account
from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.dir_models.fee import Fee
from rodManager.dir_models.payment import Payment
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class AddBillPaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Payment
        fields = [
            "user",
            "amount",
        ]

    def create(self, validated_data):
        if validated_data["amount"] == 0:
            raise serializers.ValidationError("Amount cannot be 0")
        if validated_data["amount"] < 0:
            payment = Payment.objects.create(
                user=validated_data["user"],
                type="Correction",
                date=django.utils.timezone.now().date(),
                amount=validated_data["amount"],
                description="Korekta rachunku",
            )
        else:
            payment = Payment.objects.create(
                user=validated_data["user"],
                type="BillPayment",
                date=django.utils.timezone.now().date(),
                amount=validated_data["amount"],
                description="Płatność u zarządcy",
            )
        payment.save()
        return payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "type", "date", "amount", "description", "related_fee"]


class BillPaymentView(APIView):
    @extend_schema(
        summary="Add user payments",
        description="Add user payments in the system.",
        request=AddBillPaymentSerializer,
        responses=PaymentSerializer(),
    )
    @permission_required()
    def post(self, request):
        serializer = AddBillPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PaymentSerializer(serializer.instance)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
