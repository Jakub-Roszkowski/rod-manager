from django.urls import path

import rodManager.views.payments.userComfirmPayments as listUserConfinements
import rodManager.views.payments.userPaymentsQuery as listUserPaymentsByQuery
import rodManager.views.payments.userPayments as listUserPayments
import rodManager.views.payments.payments as payments
import rodManager.views.payments.edits as edits

urlpatterns = [
    path("confirm-userspayments/<int:idUser>/", listUserConfinements.UserConfirmPaymentsView.as_view(),
         name="listUserConfirmPayments"),
    path("userspayments/<int:idUser>/", listUserPayments.UserPaymentsView.as_view(), name="listUserPayments"),
    path("userspayments/", listUserPaymentsByQuery.UserPaymentsQueryView.as_view(), name="paymentsByQuery"),
    path("", payments.PaymentsView.as_view(), name="payments"),
    path("edit-lease-fee/", edits.LeaseFeeView.as_view(), name="editLeaseFee"),
    path("edit-utility-fee/", edits.UtilityFeeView.as_view(), name="editUtilityFee"),
    path("edit-additional-fee/", edits.AdditionalFeeView.as_view(), name="editAdditionalFee"),
    path("edit-utility-values/", edits.UtilityValuesView.as_view(), name="editUtilityValues"),
    path("edit-date/", edits.DateView.as_view(), name="editDate"),

]
