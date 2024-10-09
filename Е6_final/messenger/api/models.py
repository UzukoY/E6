from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text}"