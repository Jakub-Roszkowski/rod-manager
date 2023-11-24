import os

from django.urls import include, path

import rodManager.views.accounts.account as account
import rodManager.views.accounts.accountbyid as accountbyid

urlpatterns = [
    path("", account.AccountView.as_view(), name="account"),
    path(
        "<int:account_id>/", accountbyid.AccountByIdView.as_view(), name="accountbyid"
    ),
]
