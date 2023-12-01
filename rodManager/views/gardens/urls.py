
from django.urls import path

import rodManager.views.gardens.gardenlist as gardenlist
import rodManager.views.gardens.profilefromgarden as profilefromgarden
import rodManager.views.gardens.gardens as gardens
import rodManager.views.gardens.getgarden as getgarden
urlpatterns = [

    path("gardenlist/", gardenlist.garden_list, name="gardenlist"),
    path("profile/", profilefromgarden.profile_from_garden, name="profilefromgarden"),
    path("id/", getgarden.garden_by_id, name="getgarden"),
    path("",gardens.GardensCRUD.as_view(), name="gardenCRUD")
]
