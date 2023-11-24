import os

from django.urls import include, path

import rodManager.views.announcements.announcement as announcement
import rodManager.views.announcements.announcementbyid as announcementbyid
import rodManager.views.announcements.events as events
import rodManager.views.announcements.tags as tags

urlpatterns = [
    path("announcement/", announcement.AnnouncementView.as_view(), name="image"),
    path("tag/", tags.TagView.as_view(), name="tag"),
    path("event/", events.EventView.as_view(), name="event"),
    path(
        "<int:announcement_id>/",
        announcementbyid.AnnouncementByIdView.as_view(),
        name="announcementbyid",
    ),
]
