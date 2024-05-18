from django.urls import path
from .views import *

urlpatterns = [
    # path('news_list/', index, name = 'index'),
    # path('post/<int:pk>', detail, name = 'detail'), #- было так до post_detail
    path('post/<int:pk>/', Post.as_view()), # cтало так
    path('authorlist/', AuthorList.as_view()),
    path('news/', PostList.as_view()),

]