from django import forms
from .models import *
from .views import *
from django.core.exceptions import ValidationError
from django.http import *



class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [ 'author',
                  'category_names',
                  'post_title',
                  'post_text',
       ]

   def clean(self):
       cleaned_data = super().clean()
       post_title = cleaned_data.get("post_title")
       if post_title is not None and len(post_title) < 2:
           raise ValidationError(
               "Заголовок не может быть менее 2 символов."
           )
       post_text = cleaned_data.get("post_text")
       if post_text == post_title:
           raise ValidationError(
               "Текст не должен быть идентичен заголовку."
           )
       return cleaned_data

# class PostForm(forms.Form):
#     author = forms.CharField(label='Author')
#     category_names = forms.ModelChoiceField(
#         label = 'Category', queryset=Category.objects.all(),
#     )
#     post_title = forms.CharField(label = 'Title')
#     post_text = forms.CharField(label = 'Text')
