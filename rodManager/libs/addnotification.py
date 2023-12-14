from datetime import datetime

from django.utils import timezone

from rodManager.dir_models.notification import Notification
from rodManager.libs.mailsending import send_mail_from_template


def add_notification(user, type, text, date=None, send_email=False):
    if date is None:
        date = timezone.now()
    notification = Notification.objects.create(
        user=user,
        type=type,
        date=date,
        text=text,
    )
    notification.save()
    if send_email:
        send_mail_from_template(
            "notification",
            "Nowe powiadomienie",
            user.email,
            {
                "notification": text,
            },
        )
    return notification
