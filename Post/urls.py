from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('all/', views.fetch_all_posts, name='fetch_all_posts'),
]