from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_page, name='category'),
    path('add_article/', add_article, name='add_article'),
    path('search_results/', search_results, name='search_results'),
    path('article/<int:article_id>/', article_detail, name='article'),

    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),

    path('article_update/<int:id>/', update_article, name='update'),
    path('article_delete/<int:id>/', delete_article, name='delete')
]
