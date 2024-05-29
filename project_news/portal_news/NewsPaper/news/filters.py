from django_filters import *
from .models import *
from django.forms import DateTimeInput

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category_names = ModelMultipleChoiceFilter(
        field_name='category_names',
        queryset=Category.objects.all(),
        label='Category name'
    )

    added_after = DateTimeFilter(
        field_name='post_created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'post_title': ['icontains'],
           'post_text': ['icontains'],
       }