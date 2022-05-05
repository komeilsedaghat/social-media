from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View
from .mixins import FieldMixin
from .forms import SignupUserForm,SigninUserForm,ProfileUserForm
from django.contrib.auth import get_user_model

User = get_user_model()

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


class ProfileUserView(View):
    def get(self,request,username):
        if request.user.username == username:
            user = get_object_or_404(User,username=username)
            form = ProfileUserForm(instance=user)
            return render(request,'accounts/users/self-profile.html',{'form':form})
        else:
            user = get_object_or_404(User.objects.only('username','first_name','last_name'),username=username)
            return render(request,'accounts/users/profile.html',{'user':user})
            
        
    def post(self,request,username):
        user = get_object_or_404(User,username=username)
        form = ProfileUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            username =  form.cleaned_data['username']
            return redirect('accounts:profile',username)
        return redirect('accounts:profile',username)
            