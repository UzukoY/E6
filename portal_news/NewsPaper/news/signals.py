from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings

from .models import *


@receiver(m2m_changes, sender=PostCategory)
def post_created(instance, sender, **kwargs):
    if not kwargs['action'] == 'post_created':
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.category_names.all()
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category_names.all()}'

    text_content = (
        f'Пост: {instance.post_title}\n'
        f'Текст: {instance.post_text}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Пост: {instance.post_title}<br>'
        f'Текст: {instance.post_text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()