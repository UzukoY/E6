from django_filters import FilterSet, ModelChoiceFilter

from .models import Article, UserResponse


class AdFilter(FilterSet):
    """Filters ads based on the selected author and category."""

    class Meta:
       model = Article
       fields = {'author', 'category'}


class UserResponseFilter(FilterSet):
    """Filters responses based on the ads created by the author."""
    ad = ModelChoiceFilter(
        empty_label='все объявления',
        field_name='ad',
        queryset=Article.objects.none(),
        label='Отклики на объявление'
    )

    class Meta:
       model = UserResponse
       fields = {'ad'}

    def __init__(self, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        super().__init__(*args, **kwargs)
        self.filters['ad'].queryset = Article.objects.filter(author__id=author_id)