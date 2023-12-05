from django.urls import path

import rodManager.views.complaints.changestate as change_state
import rodManager.views.complaints.complaint as complaint
import rodManager.views.complaints.complaintsbyid as complaints_by_id
import rodManager.views.complaints.message as message

urlpatterns = [
    path("", complaint.ComplaintView.as_view(), name="complaint"),
    path("message/", message.MessageView.as_view(), name="message"),
    path(
        "<int:complaint_id>/",
        complaints_by_id.ComplaintsById.as_view(),
        name="complaints-by-id",
    ),
    path(
        "changestate/<int:complaint_id>/",
        change_state.ChangeState.as_view(),
        name="change-state",
    ),
]
