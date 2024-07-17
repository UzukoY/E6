from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('news_list/', index, name = 'index'),
    # path('post/<int:pk>', detail, name = 'detail'), #- было так до post_detail
    path('post/<int:pk>/', cache_page(60*5)(PostDetail.as_view())), # cтало так
    path('authorlist/', AuthorList.as_view()),
    path('', cache_page(60)(PostList.as_view()), name = 'post_list'),
    path('create/', PostCreate.as_view(),name = 'post_create'),
    path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name = 'post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name = 'post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),

]