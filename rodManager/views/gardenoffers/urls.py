import os

from django.urls import include, path

import rodManager.views.gardenoffers.availablegardens as availablegardens
import rodManager.views.gardenoffers.gardenoffer as gardenoffers
import rodManager.views.gardenoffers.getminandmax as getminandmax

urlpatterns = [
    path("gardenoffers/", gardenoffers.GardenOfferView.as_view(), name="gardenoffers"),
    path(
        "gardenoffers/min-max/",
        getminandmax.GardenOfferMinMaxVakuesView.as_view(),
        name="gardenoffersminmax",
    ),
    path(
        "gardenoffers/available-gardens/",
        availablegardens.AvailableGardensView.as_view(),
        name="availablegardens",
    ),
]
