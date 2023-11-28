from django.urls import path

import rodManager.views.technicalProblem.technicalProblem as technical_problem



urlpatterns = [
    path("", technical_problem.TechnicalProblem.as_view(), name="technical-problem"),
]