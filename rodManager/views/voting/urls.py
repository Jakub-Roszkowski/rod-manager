from django.urls import path

import rodManager.views.voting.currentVoting as current_voting
import rodManager.views.voting.completedVoting as completed_voting
import rodManager.views.voting.createVoting as add_voting
import rodManager.views.voting.voteOnVoting as add_vote


urlpatterns = [
    path("current/", current_voting.CurrentsVotings.as_view(), name="current-voting"),
    path("completed/", completed_voting.CompletedVotings.as_view(), name="completed-voting"),
    path("add/", add_voting.AddVoting.as_view(), name="add-voting"),
    path("vote/", add_vote.VoteOnVotingAPIView.as_view(), name="add-vote")
]