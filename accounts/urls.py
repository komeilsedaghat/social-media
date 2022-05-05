from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signin/',views.SigninUserView.as_view(),name='signin'),
    path('signup/',views.SignupUserView.as_view(),name='signup'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
  
  
    path('profile/<str:username>/',views.ProfileUserView.as_view(),name='profile')
]