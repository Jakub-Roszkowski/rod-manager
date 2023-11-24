from django.urls import path

import rodManager.views.gardens.addgarden as addgarden
import rodManager.views.gardens.deletegarden as deletegarden
import rodManager.views.gardens.editgarden as editgarden
import rodManager.views.gardens.gardenlist as gardenlist
import rodManager.views.gardens.getgarden as getgarden
import rodManager.views.gardens.profilefromgarden as profilefromgarden

urlpatterns = [
    path("addgarden/", addgarden.create_garden, name="addgarden"),
    path("deletegarden/", deletegarden.delete_garden, name="deletegarden"),
    path("editgarden/", editgarden.edit_garden, name="editgarden"),
    path("gardenlist/", gardenlist.garden_list, name="gardenlist"),
    path(
        "profilefromgarden/",
        profilefromgarden.profile_from_garden,
        name="profilefromgarden",
    ),
    path("getgarden/id/", getgarden.garden_by_id, name="getgarden"),
    path("bulkgarden/", getgarden.garden_in_bulk, name="bulkgarden"),
]
