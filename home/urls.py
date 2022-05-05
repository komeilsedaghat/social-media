from .views import HomeView,AddPostView
from django.urls import path 

app_name = 'home'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('add-post/',AddPostView.as_view(),name='add-post'),
]