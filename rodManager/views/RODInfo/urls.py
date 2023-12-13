from django.urls import path

import rodManager.views.RODInfo.RODInfoApi as garden_info
import rodManager.views.RODInfo.RODDescription as garden_info_description



urlpatterns = [
    path("", garden_info.RODInfoApi.as_view(), name="RODInfo"),
    path("description/", garden_info_description.RODInfoDescriptionApi.as_view(), name="RODInfoDescription"),
    #path("<int:employer_id>/", garden_info.RODInfoApi.as_view(), name="RODInfo"),
]