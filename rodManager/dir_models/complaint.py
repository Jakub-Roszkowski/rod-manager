from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status

from rodManager.dir_models.account import Account


class ComplaintStatus(models.TextChoices):
    REPORTED = "Reported", _("Zgłoszono")
    ACCEPTED = "Accepted", _("Przyjęto")
    INPROGRESS = "InProgress", _("W trakcie")
    COMPLETE = "Complete", _("Zakończono")
    REJECTED = "Rejected", _("Odrzucono")


class MessageAuthor(models.TextChoices):
    USER = "USER", _("Użytkownik")
    MANAGER = "MANAGER", _("Zarządca")


class Complaint(models.Model):
    title = models.CharField(max_length=255)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.REPORTED,
    )
    user = models.ForeignKey(
        Account, related_name="complaints", on_delete=models.CASCADE
    )
    manager = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    un_read_user = models.CharField(
        max_length=20,
        choices=MessageAuthor.choices,
        default=MessageAuthor.MANAGER,
        null=True,
    )

    def last_update_date(self):
        if self.messages.all().last().creation_date:
            return self.messages.all().last().creation_date
        else:
            return self.open_date


class Message(models.Model):
    complaint = models.ForeignKey(
        Complaint, related_name="messages", on_delete=models.CASCADE
    )
    author = models.CharField(
        max_length=20,
        choices=MessageAuthor.choices,
        default=MessageAuthor.USER,
    )
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "author",
            "content",
            "creation_date",
        ]


class ComplaintSerializer(serializers.ModelSerializer):
    submitter = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id",
            "title",
            "open_date",
            "close_date",
            "last_update_date",
            "state",
            "submitter",
            "user",
            "manager",
            "messages",
        ]

    def get_user(self, obj):
        return obj.user.email

    def get_manager(self, obj):
        if obj.manager:
            return obj.manager.email
        else:
            return None

    def get_submitter(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


class ComplainsWithoutMassagesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    readed = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            "id",
            "title",
            "open_date",
            "close_date",
            "last_update_date",
            "state",
            "user",
            "manager",
            "readed",
        ]

    def get_user(self, obj):
        return obj.user.email

    def get_manager(self, obj):
        if obj.manager:
            return obj.manager.email
        else:
            return None

    def get_readed(self, obj):
        if self.context["request"].user == obj.user:
            if obj.un_read_user == MessageAuthor.USER:
                return False
            else:
                return True
        else:
            if obj.un_read_user == MessageAuthor.MANAGER:
                return False
            else:
                return True
