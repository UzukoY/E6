from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', context={'posts': posts})

def detail(request, pk):
    post = Post.objects.get(pk__iexact=pk)
    return render(request, "details.html", context={'post': post.post_text})


# class AuthorList(ListView):
#     # Указываем модель, объекты которой мы будем выводить
#     model = Author
#     # Поле, которое будет использоваться для сортировки объектов
#     ordering = 'author_user'
#     # Указываем имя шаблона, в котором будут все инструкции о том,
#     # как именно пользователю должны быть показаны наши объекты
#     template_name = 'products.html'
#     # Это имя списка, в котором будут лежать все объекты.
#     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
#     context_object_name = 'products'