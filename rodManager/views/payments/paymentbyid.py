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
from rodManager.dir_models.payment import Payment
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class AddPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "user",
            "type",
            "date",
            "amount",
            "description",
        ]

    def create(self, validated_data):
        payment = Payment.objects.create(
            user=validated_data["user"],
            type=validated_data["type"],
            date=validated_data["date"],
            amount=validated_data["amount"],
            description=validated_data["description"],
        )
        payment.save()
        return payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "type", "date", "amount", "description", "related_fee"]


class PaymentByIdView(APIView):
    @extend_schema(
        summary="Add fee",
        description="Add fee in the system.",
        responses=PaymentSerializer(),
    )
    @permission_required()
    def get(self, request, user_id):
        if user_id is None:
            return Response(
                {"error": "user_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        payments = Payment.objects.filter(user=user_id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
