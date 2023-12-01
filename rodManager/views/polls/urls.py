from django.urls import path

import rodManager.views.polls.completedPolls as completed_polls
import rodManager.views.polls.createPoll as add_poll
import rodManager.views.polls.currentPolls as current_polls
import rodManager.views.polls.voteOnPoll as add_vote

urlpatterns = [
    path("current/", current_polls.CurrentsPolls.as_view(), name="current-polls"),
    path(
        "completed/",
        completed_polls.CompletedPolls.as_view(),
        name="completed-polls",
    ),
    path("", add_poll.CreatePoll.as_view(), name="create-poll"),
    path("vote/", add_vote.VoteOnPoll.as_view(), name="add-vote"),
]
