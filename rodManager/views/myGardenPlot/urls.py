from django.urls import path

import rodManager.views.myGardenPlot.myGarden as myGarden


urlpatterns = [
    path("", myGarden.MyGardenAPI.as_view(), name="current-voting"),
]