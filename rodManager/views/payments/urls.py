from django.urls import path

import rodManager.views.payments.billingperiod as billingperiod
import rodManager.views.payments.confirmbillingperiod as confirmbillingperiod
import rodManager.views.payments.editfeebyid as editfeebyid
import rodManager.views.payments.edits as edits
import rodManager.views.payments.fee as fee
import rodManager.views.payments.feebyid as feebyid
import rodManager.views.payments.paymentbyid as paymentbyid
import rodManager.views.payments.paymentt as paymentt

urlpatterns = [
    path(
        "billingperiod/",
        billingperiod.BillingPeriodView.as_view(),
        name="billingperiod",
    ),
    path(
        "billingperiod/confirm/<billing_period_id>/",
        confirmbillingperiod.ConfirmBillingPeriodView.as_view(),
        name="confirmbillingperiod",
    ),
    path("fee/", fee.FeeView.as_view(), name="fee"),
    path("<billing_period_id>/", feebyid.FeeByIdView.as_view(), name="feeById"),
    path("fee/<fee_id>/", editfeebyid.EditFeeByIdView.as_view(), name="editFeeById"),
    path("paymentt/", paymentt.PaymenttView.as_view(), name="payment"),
    path(
        "payment/<user_id>/", paymentbyid.PaymentByIdView.as_view(), name="paymentById"
    ),
]
