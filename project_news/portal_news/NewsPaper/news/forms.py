from django import forms
from .models import *
from .views import *


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [ 'author',
                  'category_names',
                  'post_title',
                  'post_text',
       ]

class PostForm(forms.Form):
    author = forms.CharField(label='Author')
    category_names = forms.ModelChoiceField(
        label = 'Category', queryset=Category.objects.all(),
    )
    post_title = forms.CharField(label = 'Title')
    post_text = forms.CharField(label = 'Text')
