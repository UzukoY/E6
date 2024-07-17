from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import *
from .forms import *
from django.http import *
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views import View
from .tasks import *
from .signals import *

from django.core.cache import cache # импортируем наш кэш


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

class PostDetail(DetailView): #принимает только 1 объект
    model = Post
    context_object_name = 'Post'

class PostList(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'flatpages/news.html'
    ordering = '-post_created'
    paginate_by = 10 # количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect('/news/')
    else:
        form = PostForm()
        context = { 'form': form, }
        return render(request, 'posts_edit.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ("news.add_post",)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    permission_required = ("news.change_post",)
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'


class PostDelete(DeleteView):
    permission_required = ("news.delete_post",)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

# для отображения celery tasks:
class IndexView(View):
    def get(self, request):
        add.delay()
        return HttpResponse('Hello!')


class ProductDetailView(DetailView):
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj