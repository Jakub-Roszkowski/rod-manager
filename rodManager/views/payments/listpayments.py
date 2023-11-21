from rest_framework.views import APIView
from rest_framework.response import Response
from dir_models.payment import Payment
from rest_framework import serializers

class ListPaymentsView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        