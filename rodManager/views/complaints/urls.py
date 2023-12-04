from django.urls import path

import rodManager.views.complaints.complaint as complaint
import rodManager.views.complaints.message as message

urlpatterns = [
    path("", complaint.ComplaintView.as_view(), name="complaint"),
    path("message/", message.MessageView.as_view(), name="message"),
]
