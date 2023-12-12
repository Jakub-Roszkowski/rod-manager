from django.urls import path

import rodManager.views.gardeners.gardeners as gardeners

urlpatterns = [
    path("", gardeners.AccountView.as_view(), name="gardeners"),
]
