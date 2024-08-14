from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save

from .models import *


@reciever(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    mail = instance.author.email
    send_mail(
        'Subject',
        'Some message',
        'sf.news.notification@yandex.ru',
        [mail],
        fail_silently=False,
    )
