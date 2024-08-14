from django import forms
from django.core.exceptions import ValidationError

from .models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('author', 'category', 'title', 'text',)
        exclude = ['dateCreation']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок"
        self.fields['text'].label = "Текст объявления:"

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Объявление не может быть менее 20 символов."
            })

        return cleaned_data


class RespondForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(RespondForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"