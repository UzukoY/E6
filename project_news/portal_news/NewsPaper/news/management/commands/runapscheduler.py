import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import *

logger = logging.getLogger(__name__)


def my_job():
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


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")