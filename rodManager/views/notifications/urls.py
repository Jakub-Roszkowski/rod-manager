from django.urls import path

import rodManager.views.notifications.newnotification as newnotification
import rodManager.views.notifications.notification as notification
import rodManager.views.notifications.readnotification as readnotification

urlpatterns = [
    path(
        "",
        notification.NotificationView.as_view(),
        name="notifications",
    ),
    path(
        "read/<int:notification_id>/",
        readnotification.ReadNotificationView.as_view(),
        name="readnotifications",
    ),
    path(
        "new/", newnotification.NewNotificationView.as_view(), name="newnotifications"
    ),
]
