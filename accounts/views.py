from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import SignupUserForm,SigninUserForm

class SigninUserView(LoginView):
    template_name = "accounts/registrations/sign_in.html"
    form_class = SigninUserForm
    success_message = "You Logined successfully"

    def get_success_url(self):
        return reverse_lazy('home:home')


class SignupUserView(CreateView):
    template_name = 'accounts/registrations/sign_up.html'
    success_url = reverse_lazy('accounts:signin')
    form_class = SignupUserForm
    success_message = "Your profile was created successfully"


class LogoutUserView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
