from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import *
from .tasks import *


# Для отправки уведомлений о новых постах через селери:
@receiver(m2m_changed, sender=PostCategory)
def send_email(instance, sender, **kwargs):
    if kwargs['action'] == 'post_add':
        send_email_task.delay(instance.pk)