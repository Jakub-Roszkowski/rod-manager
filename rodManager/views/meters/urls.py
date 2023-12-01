from django.urls import path
from rodManager.views.meters.meters import MetersCRUD
from rodManager.views.meters.records import RecordsCRUD

urlpatterns = [
    path('meters/', MetersCRUD.as_view()),
    path("records/", RecordsCRUD.as_view()),
]
