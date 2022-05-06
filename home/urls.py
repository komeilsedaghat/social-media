from .views import HomeView,AddPostView,DeletePostView
from django.urls import path 

app_name = 'home'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('add-post/',AddPostView.as_view(),name='add-post'),
    path('delete-post/<str:username>/<str:slug>/',DeletePostView.as_view(),name='delete-post'),
]