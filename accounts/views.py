from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login 
from django.views.generic import View
from django.contrib import messages
import random
from django.conf import settings
from accounts.models import OtpCode
from .mixins import FieldMixin
from .forms import SignupUserForm,SigninUserForm,ProfileUserForm,SigninVerifyForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



class SigninUserView(View):
    template_name = 'accounts/registrations/sign_in.html'
    def get(self,request):
        form = SigninUserForm
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.TFA == True:
                random_code = random.randint(1000,9999)
                if user.email:

                    #send email
                    subject = 'Verify Code'
                    message = f" Hi '{username}' Your Verify Code:{random_code}\n Have a Good Day"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email,]    
                    send_mail( subject, message, email_from, recipient_list )
                    
                    TFA_code = OtpCode.objects.create(code=random_code,email=user.email)
                    request.session['user_registration_info'] = {
                        'username':username,
                        'password':password,
                        'random_code':random_code
                }
                return redirect('accounts:verify')
            else:
                login(request,user)
                messages.success(request,'You Logined Successfully!')
                return redirect('home:home')
        else:
            messages.error(request,'your username or password is wrong')
            return redirect('accounts:signin')



class SigninVerifyCodeView(View):
    template_name = 'accounts/registrations/signin_verify.html'
    def get(self,request):
        form = SigninVerifyForm
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        user_sesstion = request.session['user_registration_info']
        form = SigninVerifyForm(request.POST)
        if form.is_valid():
            code = user_sesstion['random_code']
            input_code = form.cleaned_data['code']
            if code == input_code:
                user = authenticate(request, username=user_sesstion['username'], password=user_sesstion['password'])
                login(request,user)
                OtpCode.objects.filter(code=input_code).delete()
                return redirect('home:home')
            else:
                messages.error(request,'Your Verify Code is Wrong Please Try Again')
                return redirect('accounts:verify')


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
            