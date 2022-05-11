from .views import HomeView,AddPostView,DeletePostView,UpdatePostView,CommentPostView,MessagesProfileView,AcceptCommentView
from django.urls import path 

app_name = 'home'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('add-post/',AddPostView.as_view(),name='add-post'),
    path('delete-post/<str:username>/<str:slug>/<int:pk>/',DeletePostView.as_view(),name='delete-post'),
    path('edit-post/<str:username>/<str:slug>/<int:pk>/',UpdatePostView.as_view(),name='edit-post'),
    path('comments/<str:username>/<str:slug>/<int:pk>/',CommentPostView.as_view(),name='comment'),
    path('messages/',MessagesProfileView.as_view(),name='messages'),
    path('accept-message/<int:pk>/',AcceptCommentView.as_view(),name='accept-comment')

]