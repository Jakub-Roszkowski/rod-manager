
from django.urls import include, path
import os
import rodManager.views.gardens.addgarden as addgarden
import rodManager.views.gardens.deletegarden as deletegarden
import rodManager.views.gardens.editgarden as editgarden
import rodManager.views.gardens.gardenlist as gardenlist
import rodManager.views.gardens.profilefromgarden as profilefromgarden
import rodManager.views.gardens.getgarden as getgarden

urlpatterns = [
    path("addgarden/", addgarden., name="addgarden"),
    path("deletegarden/", deletegarden.DeleteGardenView.as_view(), name="deletegarden"),
    path("editgarden/", editgarden.EditGardenView.as_view(), name="editgarden"),
    path("gardenlist/", gardenlist.garden_list.as_view(), name="gardenlist"),
    path("profilefromgarden/", profilefromgarden.profile_from_garden.as_view(), name="profilefromgarden"),
    path("getgarden/id", getgarden.garden_by_id.as_view(), name="getgarden"),
]
