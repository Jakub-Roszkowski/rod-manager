from django.urls import path

import rodManager.views.voting.currentVoting as current_voting
import rodManager.views.voting.completedVoting as completed_voting
import rodManager.views.voting.completedVoting as add_voting


urlpatterns = [
    path("current/", current_voting.CurrentsVotings.as_view(), name="current-voting"),
    path("completed/", completed_voting.CurrentsVotings.as_view(), name="completed-voting"),
    path("add/", add_voting.CurrentsVotings.as_view(), name="add-voting"),
]