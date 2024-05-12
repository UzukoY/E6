from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.DecimalField(default=0, decimal_places=2, max_digits=5)  # 2 знака после запятой

    def update_rating(self):
        posts_rate = self.post_set.aggregate(total_P_rating=Sum('post_rating'))
        pRat = 0
        pRat += posts_rate.get('total_P_rating')

        comment_rate = self.author_user.comment_set.aggregate(total_C_rating=Sum('post_rating'))
        cRat = 0
        cRat += comment_rate.get('total_C_rating')

        self.author_rating = pRat *3 + cRat
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True) # Принято выбирать число по прогрессии 2-4-8-16-32-64...


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)  # Чтобы с удалением автора не удалялись его статьи
    news_post = 'NE'
    article = 'AR'
    POST_TYPES = [
        (news_post, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news_post)
    post_created = models.DateTimeField(auto_now_add=True) # Автоматическое добавление даты создания
    category_names = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=256)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return '{} ... {}'.format(self.post_text[0:128], str(self.post_rating))


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()
