from django.urls import path

import rodManager.views.gardenInfo.gardenInfoApi as garden_info
import rodManager.views.gardenInfo.gardenDescription as garden_info_description



urlpatterns = [
    path("", garden_info.GardenInfoApi.as_view(), name="GardenInfo"),
    path("description/", garden_info_description.GardenInfoDescriptionApi.as_view(), name="GardenInfoDescription"),
    path("<int:employer_id>/", garden_info.GardenInfoApiWithID.as_view(), name="GardenInfo"),
]