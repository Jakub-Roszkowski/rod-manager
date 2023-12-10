from django.db import models
from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
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
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class BalanceSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["id", "balance"]

    def get_balance(self, obj):
        return obj.calculate_balance()


class BalanceByIdView(APIView):
    @extend_schema(
        summary="Get balance",
        description="Get balance of an accounts.",
        responses=BalanceSerializer,
    )
    def get(self, request, user_id):
        account = get_object_or_404(Account, pk=user_id)
        serializer = BalanceSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
