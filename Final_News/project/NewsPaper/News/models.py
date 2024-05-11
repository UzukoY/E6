from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    User_rating = models.DecimalField(default=0, decimal_places=2, max_digits=5)  # 2 знака после запятой

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_set = None

    def update_rating(self):
        # Суммарный рейтинг каждой статьи автора умножается на 3
        posts_rate = self.post_set.aggregate(total_rate=Sum('post_rating'))['total_rate'] or 0
        posts_rate *= 3

        # Суммарный рейтинг всех комментариев автора
        comments_rate = self.author.comment_set.aggregate(total_rating=Sum('comment_rating'))['total_rating'] or 0

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comments_rate = \
            Comment.objects.filter(related_post__author=self).aggregate(total_rating=Sum('comment_rating'))[
                'total_rating'] or 0

        # Обновление рейтинга автора
        self.user_rating = posts_rate + comments_rate + post_comments_rate
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)  # Чтобы с удалением автора не удалялись его статьи
    news_post = 'NE'
    article = 'AR'

    POST_TYPES = [
        (news_post, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news_post)
    post_created = models.DateTimeField(auto_now_add=True)
    category_names = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.post_text) > 124:
            preview_text = self.post_text[:124] + '...'
            return preview_text
        else:
            return self.post_text


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
