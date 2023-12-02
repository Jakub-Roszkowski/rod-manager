from django.db import models
from django.utils.translation import gettext_lazy as _


class ComplaintStatus(models.TextChoices):
    REPORTED = "Reported", _("Zgłoszono")
    ACCEPTED = "Accepted", _("Przyjęto")
    INPROGRESS = "InProgress", _("W trakcie")
    COMPLETE = "Complete", _("Zakończono")
    REJECTED = "Rejected", _("Odrzucono")


class Complaint(models.Model):
    title = models.CharField(max_length=255)
    opening_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.REPORTED,
    )


class Message(models.Model):
    complaint = models.ForeignKey(
        Complaint, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        Account, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
