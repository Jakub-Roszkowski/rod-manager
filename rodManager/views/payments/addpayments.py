
from dir_models.payment import Payment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddPaymentView(APIView):
    def post(request):
        if "rodManager.managePayments" not in request.user.get_all_permissions():
            return Response({"error": "You don't have permission to add payments."}, status=status.HTTP_403_FORBIDDEN)
        if not request.data["leaseholderID"] or not request.data["amount"] or not request.data["date"]:
            return Response({"error": "leaseholderID, amount and date are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data["leaseholderID"].isdigit():
            return Response({"error": "leaseholderID must be a number."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data["amount"].isdigit():
            return Response({"error": "amount must be a number."}, status=status.HTTP_400_BAD_REQUEST)
        if not Payment.objects.filter(leaseholderID=request.data["leaseholderID"]).exists():
            return Response({"error": "Leaseholder doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.create(
            leaseholderID=request.data["leaseholderID"],
            amount=request.data["amount"],
            date=request.data["date"],
        )
        payment.save()
        return Response({"success": "Payment added successfully."}, status=status.HTTP_201_CREATED)