from django.urls import path

import rodManager.views.documents.document as document
import rodManager.views.documents.documentbyid as documentbyid

urlpatterns = [
    path("", document.DocumentView.as_view(), name="document"),
    path(
        "<int:document_id>/",
        documentbyid.DocumentByIdView.as_view(),
        name="documentbyid",
    ),
]
