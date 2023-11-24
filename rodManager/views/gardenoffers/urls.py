import os

from django.urls import include, path

import rodManager.views.gardenoffers.availablegardens as availablegardens
import rodManager.views.gardenoffers.contact as contact
import rodManager.views.gardenoffers.gardenoffer as gardenoffers
import rodManager.views.gardenoffers.getminandmax as getminandmax

urlpatterns = [
    path("", gardenoffers.GardenOfferView.as_view(), name="garden-offers"),
    path(
        "min-max/",
        getminandmax.GardenOfferMinMaxVakuesView.as_view(),
        name="gardenoffersminmax",
    ),
    path(
        "available-gardens/",
        availablegardens.AvailableGardensView.as_view(),
        name="availablegardens",
    ),
    path("contact/", contact.ContactView.as_view(), name="contact"),
]
