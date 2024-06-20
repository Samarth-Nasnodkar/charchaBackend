from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetchUser, name='fetch_user'),
    path('all/', views.fetchAllUsers, name='fetch_all_users'),
    path('update/', views.updateUser, name='update_user'),
]