from django.urls import path
from . import views

urlpatterns = [
    path('username/<str:username>', views.fetchUser, name='fetch_user'),
    path('all/', views.fetchAllUsers, name='fetch_all_users'),
    path('update/', views.updateUser, name='update_user'),
    path('delete/', views.deleteUser, name='delete_user'),
]
