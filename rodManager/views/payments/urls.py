from django.urls import path

import rodManager.views.payments.addpayments as addpayments
import rodManager.views.payments.listpayments as listpayments

urlpatterns = [
    path("addpayment/", addpayments.AddPaymentView.as_view(), name="addpayment"),
    path("listpayments/", listpayments.ListPaymentsView.as_view(), name="listpayments"),
]
