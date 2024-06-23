from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createComment, name='create_comment'),
    path('all/', views.fetchAllComments, name='fetch_all_comments'),
    path('post/<str:post_id>', views.fetchCommentsByPost, name='fetch_post_comments'),
    path('user/<str:author_username>', views.fetchCommentsByAuthor, name='fetch_user_comments'),
]