from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', context={'posts': posts})

# def detail(request, pk):
#     post = Post.objects.get(pk__iexact=pk)
#     return render(request, "details.html", context={'post': post.post_text})


class AuthorList(ListView): # работает со списком
    # Указываем модель, объекты которой мы будем выводить
    model = Author # равен queryset = Author.objects.all(), но здесь мы можем включить фильтр/сортировку
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'author_user'
    # # Указываем имя шаблона, в котором будут все инструкции о том,
    # # как именно пользователю должны быть показаны наши объекты
    template_name = 'author_list.html'
    # # Это имя списка, в котором будут лежать все объекты.
    # # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Authors'

class Post(DetailView): #принимает только 1 объект
    model = Post
    context_object_name = 'Post'

class PostList(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'NewsPaper/templates/flatpages/news.html'
    ordering = 'post_created'


