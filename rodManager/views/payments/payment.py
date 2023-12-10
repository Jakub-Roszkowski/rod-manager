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


class AddPaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    type = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    amount = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)

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


class PaymentView(APIView):
    @extend_schema(
        summary="Add user payments",
        description="Add user payments in the system.",
        request=AddPaymentSerializer,
        responses=PaymentSerializer(),
    )
    @permission_required()
    def post(self, request):
        serializer = AddPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
