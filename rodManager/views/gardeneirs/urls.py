from django.urls import path

import rodManager.views.gardeneirs.gardeneirs as gardeneirs

urlpatterns = [
    path("", gardeneirs.AccountView.as_view(), name="gardeneirs"),
]
