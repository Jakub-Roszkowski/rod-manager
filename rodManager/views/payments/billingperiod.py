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
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    payment_date = serializers.DateField()

    class Meta:
        model = BillingPeriod
        fields = ["start_date", "end_date", "payment_date"]

    def create(self, validated_data):
        billingperiod = BillingPeriod.objects.create(
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            payment_date=validated_data["payment_date"],
        )
        billingperiod.save()
        return billingperiod


class BillingPeriodView(APIView):
    pagination_class = RODPagination

    @extend_schema(
        summary="Get billingperiod",
        description="Get billingperiod in the system.",
        parameters=[
            OpenApiParameter(name="page", type=OpenApiTypes.INT),
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
        ],
        responses=BillingPeriodSerializer(many=True),
    )
    # @permission_required()
    def get(self, request):
        billingperiod = BillingPeriod.objects.all().order_by("-start_date")
        paginator = RODPagination()
        page = paginator.paginate_queryset(billingperiod, request)
        serializer = BillingPeriodSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Add billingperiod",
        description="Add billingperiod to the system.",
        request=AddBillingPeriodSerializer,
        responses=BillingPeriodSerializer,
    )
    # @permission_required()
    def post(self, request):
        serializer = AddBillingPeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
