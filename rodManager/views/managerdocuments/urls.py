from django.urls import path

import rodManager.views.managerdocuments.document as document
import rodManager.views.managerdocuments.documentbyid as documentbyid

urlpatterns = [
    path("", document.ManagerDocumentView.as_view(), name="managerdocument"),
    path(
        "<int:document_id>/",
        documentbyid.ManagerDocumentByIdView.as_view(),
        name="documentbyid",
    ),
]
