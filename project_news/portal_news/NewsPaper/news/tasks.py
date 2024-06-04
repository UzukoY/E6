from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives, send_mail, mail_managers
from .models import *
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category_names.all()
    title = post.post_title
    subscribers_emails = [] #все подписчики на все категории

    for category in categories:
        subscribers_emails += list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))

    html_content = (
        f'Пост: {post.post_title}<br>'
        f'Текст: {post.post_text}<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=set(subscribers_emails),
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_created__gte=last_week)
    categories = set(post.category_names.values_list('category_name', flat=True) for post in posts)
    subscribers = set(User.objects.filter(subscriptions__category__category_name__in=categories))

    for user in subscribers:
        sub_cat = user.subscriptions.values_list('category__category_name', flat = True)
        posts_sub_cat = posts.filter(category_names__category_name__in=sub_cat)

        message = f'Здравствуй, {user.username}!\n\nНовые посты за неделю: \n\n'
        for post in posts_sub_cat:
            message += f'{post.post_title}\n'
            message += f'URL: http://127.0.0.1:8000{post.get_absolute_url()}\n\n'

        send_mail(
            'Новости недели',
            message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    posts_for_managers = Post.objects.order_by('-post_created')[:10]
    text_for_managers = '\n'.join(['{} - {}'.format(p.post_title, p.post_text) for p in posts_for_managers])
    mail_managers("Самые последние статьи", text_for_managers)