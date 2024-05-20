from django.urls import path
from . import views

urlpatterns = [	
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('edit_photo_profile', views.edit_photo_profile, name='edit_photo_profile'),
    path('addComment', views.addComment, name='addComment'),
    path('add_post', views.add_post, name='add_post'),
    path('like_post', views.like_post, name='like_post'),
    path('Follow_user', views.Follow_user, name='Follow_user'),
    path('search', views.search, name='search'),
    path('PostDelete', views.PostDelete, name='PostDelete'),
    path('addPost', views.addPost, name='addPost'),
    path('PostDetails', views.PostDetails, name='PostDetails'),


]