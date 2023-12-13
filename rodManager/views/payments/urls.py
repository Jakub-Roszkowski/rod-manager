from django.urls import path

import rodManager.views.payments.billingperiod as billingperiod
import rodManager.views.payments.billingperiodbyid as billingperiodbyid
import rodManager.views.payments.billpayment as billpayment
import rodManager.views.payments.confirmbillingperiod as confirmbillingperiod
import rodManager.views.payments.currentfee as currentfee
import rodManager.views.payments.editfeebyid as editfeebyid
import rodManager.views.payments.edits as edits
import rodManager.views.payments.fee as fee
import rodManager.views.payments.feebyid as feebyid
import rodManager.views.payments.payment as payment
import rodManager.views.payments.paymentbyid as paymentbyid

urlpatterns = [
    path(
        "billing-period/",
        billingperiod.BillingPeriodView.as_view(),
        name="billing period",
    ),
    path(
        "billing-period/confirm/<billing_period_id>/",
        confirmbillingperiod.ConfirmBillingPeriodView.as_view(),
        name="confirmbillingperiod",
    ),
    path("fee/", fee.FeeView.as_view(), name="fee"),
    path("fee/current/", currentfee.CurrentFeeView.as_view(), name="current fee"),
    path(
        "fee/by-billing-period/<billing_period_id>/",
        feebyid.FeeByIdView.as_view(),
        name="feeById",
    ),
    path(
        "fee/by-id/<fee_id>/", editfeebyid.EditFeeByIdView.as_view(), name="editFeeById"
    ),
    path("payment/", payment.PaymentView.as_view(), name="payment"),
    path("bill-payment/", billpayment.BillPaymentView.as_view(), name="bill payment"),
    path(
        "payment/<user_id>/", paymentbyid.PaymentByIdView.as_view(), name="paymentById"
    ),
    path(
        "billing-period/by-id/<billing_period_id>/",
        billingperiodbyid.BillingPeriodByIdView.as_view(),
        name="billingperiodbyid",
    ),
]
