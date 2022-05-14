from . import views
from django.urls import path 

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('add-post/',views.AddPostView.as_view(),name='add-post'),
    path('delete-post/<str:username>/<str:slug>/<int:pk>/',views.DeletePostView.as_view(),name='delete-post'),
    path('edit-post/<str:username>/<str:slug>/<int:pk>/',views.UpdatePostView.as_view(),name='edit-post'),
    path('comments/<str:username>/<str:slug>/<int:pk>/',views.CommentPostView.as_view(),name='comment'),
    path('messages/',views.MessagesProfileView.as_view(),name='messages'),
    path('accept-message/<int:pk>/',views.AcceptCommentView.as_view(),name='accept-comment'),

]