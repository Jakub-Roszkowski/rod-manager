from django.urls import path

import rodManager.views.userdocuments.document as document
import rodManager.views.userdocuments.documentbyid as documentbyid
import rodManager.views.userdocuments.documentbyuserid as documentbyuserid

urlpatterns = [
    path("", document.UserDocumentView.as_view(), name="userdocument"),
    path(
        "by-document-id/<int:document_id>/",
        documentbyid.UserDocumentByIdView.as_view(),
        name="documentbyid",
    ),
    path(
        "by-user-id/<int:user_id>/",
        documentbyuserid.UserDocumentByUserIdView.as_view(),
        name="documentbyuserid",
    ),
]
