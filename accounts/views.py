from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login 
from django.views.generic import View
from django.contrib import messages
import random
from django.conf import settings
from accounts.models import FollowUserModel, OtpCode
from django.contrib.auth import views
from .forms import SignupUserForm,SigninUserForm,ProfileUserForm,SigninVerifyForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from home.models  import PostModel

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


class PassChangeView(LoginRequiredMixin,views.PasswordChangeView):
    template_name ='accounts/registrations/password_change/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class PassChangeDoneView(LoginRequiredMixin,views.PasswordChangeDoneView):
    template_name ='accounts/registrations/password_change/password_change_done.html'
    success_url = reverse_lazy('accounts:signin')




class PassResetView(LoginRequiredMixin,views.PasswordResetView):
    template_name = 'accounts/registrations/password_reset/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/registrations/password_reset/password_reset_email.html'


class PassResetDoneView(LoginRequiredMixin,views.PasswordResetDoneView):
   template_name = 'accounts/registrations/password_reset/password_reset_done.html'


class PassResetConfirm(LoginRequiredMixin,views.PasswordResetConfirmView):
    template_name = 'accounts/registrations/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PassResetComplete(LoginRequiredMixin,views.PasswordResetCompleteView):
    template_name = 'accounts/registrations/password_reset/password_reset_complete.html'



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
            print(100*';')
            print(request.user.blocked_users)
            is_following = False
            if FollowUserModel.objects.filter(from_user=request.user,to_user=user).exists():
                is_following = True
            follower=FollowUserModel.objects.filter(to_user = user).count()
            following = FollowUserModel.objects.filter(from_user = user).count()
            posts = PostModel.objects.filter(author=user).count()
            context ={
                'follower':follower,
                'following':following,
                'post':posts,
                'is_following':is_following,
                'user':user,
            }
            return render(request,'accounts/users/profile.html',context)

            
        
    def post(self,request,username):
        user = get_object_or_404(User,username=username)
        form = ProfileUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            username =  form.cleaned_data['username']
            return redirect('accounts:profile',username)
        return redirect('accounts:profile',username)
            

class BlockUserView(LoginRequiredMixin,View):
    def get(self,request,username):
        user = User.objects.get(username=username)
        if user is not None:
            request.user.blocked_users.add(user)
            messages.success(request,f"User '{username}' Blocked Successfully ")
            return redirect('home:home')


class FollowUserView(View):
    def post(self,request):
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = FollowUserModel.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status':'exists'})
        else:
            FollowUserModel(from_user=request.user, to_user=following).save()
            return JsonResponse({'status':'ok'})


class UnFollowUserView(View):
    def post(self,request):
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = FollowUserModel.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'notexists'})


