from django.urls import path

import rodManager.views.pools.completedPools as completed_pools
import rodManager.views.pools.createPool as add_pool
import rodManager.views.pools.currentPools as current_pools
import rodManager.views.pools.voteOnPool as add_vote

urlpatterns = [
    path("current/", current_pools.CurrentsPools.as_view(), name="current-pools"),
    path(
        "completed/",
        completed_pools.CompletedPools.as_view(),
        name="completed-polls",
    ),
    path("", add_pool.CreatePool.as_view(), name="create-pool"),
    path("vote/", add_vote.VoteOnPool.as_view(), name="add-vote"),
]
