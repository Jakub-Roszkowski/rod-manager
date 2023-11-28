from django.urls import path

import rodManager.views.gardenInfo.gardenInfoApi as garden_info



urlpatterns = [
    path("", garden_info.GardenInfoApi.as_view(), name="GardenInfo"),
    path("<int:employer_id>/", garden_info.GardenInfoApiWithID.as_view(), name="GardenInfo"),
]