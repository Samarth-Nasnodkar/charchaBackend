from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('all/', views.fetch_all_posts, name='fetch_all_posts'),
    path('author/<str:username>', views.fetch_posts_by_author, name='fetch_author_posts'),
    path('p/<str:post_id>', views.fetch_post, name='fetch_post'),
]