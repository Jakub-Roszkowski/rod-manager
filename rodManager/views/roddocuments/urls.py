from django.urls import path

import rodManager.views.roddocuments.document as document
import rodManager.views.roddocuments.documentbyid as documentbyid

urlpatterns = [
    path("", document.RodDocumentView.as_view(), name="roddocument"),
    path(
        "<int:document_id>/",
        documentbyid.RodDocumentByIdView.as_view(),
        name="documentbyid",
    ),
]
