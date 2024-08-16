import datetime

from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Article(models.Model):
    TYPE = (
        ('TA', 'Танки'),
        ('HE', 'Хилы'),
        ('DD', 'ДД'),
        ('BU', 'Торговцы'),
        ('GM', 'Гильдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TA', 'Кожевники'),
        ('PM', 'Зевлевары'),
        ('SM', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = CKEditor5Field(verbose_name='Текст', config_name='extends', null=True, blank=True)
    category = models.CharField(max_length=2, choices=TYPE, default='TA')
    upload=models.FileField(upload_to='uploads/')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def get_absolute_url(self):
        return reverse('Article_detail', args=[str(self.id)])


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='responses')
    text = CKEditor5Field(verbose_name='Текст', config_name='extends', null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.text[:20]}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'