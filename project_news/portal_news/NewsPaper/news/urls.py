from django.urls import path
from .views import *

urlpatterns = [
    # path('news_list/', index, name = 'index'),
    # path('post/<int:pk>', detail, name = 'detail'), #- было так до post_detail
    path('post/<int:pk>/', PostDetail.as_view()), # cтало так
    path('authorlist/', AuthorList.as_view()),
    path('', PostList.as_view()),
    path('create/', create_post,name = 'post_create'),
]