from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signin/',views.SigninUserView.as_view(),name='signin'),
    path('signin/verify/',views.SigninVerifyCodeView.as_view(),name='verify'),
    path('signup/',views.SignupUserView.as_view(),name='signup'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),

    #password change
    path('password-change/',views.PassChangeView.as_view(),name='password_change'),
    path('password-change-done/',views.PassChangeDoneView.as_view(),name='password_change_done'),

    #password reset
    path('password-reset/',views.PassResetView.as_view(),name='password_reset'),
    path('password-reset/done/',views.PassResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',views.PassResetConfirm.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/',views.PassResetComplete.as_view(),name='password_reset_complete'),
  
  
    path('profile/<str:username>/',views.ProfileUserView.as_view(),name='profile')
]