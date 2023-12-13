from django.urls import path

import rodManager.views.passwordreset.confirm as confirm
import rodManager.views.passwordreset.request as request

urlpatterns = [
    path("request/", request.PaswordResetRequestView.as_view(), name="passwordreset"),
    path("confirm/", confirm.PaswordResetConfirmView.as_view(), name="passwordreset"),
]
