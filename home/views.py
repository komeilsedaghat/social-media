from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import CommentModel, PostModel,CategoryModel, ReportPostModel
from django.views import generic
from .forms import AddPostForm, CommentForm, CommentMessagesForm, ReportPostForm
from django.contrib.auth import get_user_model
from .mixins import AuthorAccessMixin, SuperUserAuthorAccessMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
# Create your views here.

User = get_user_model()


class HomeView(LoginRequiredMixin,View):
    
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        user_blocked = user.blocked_users.all()
        context = {
            'posts':PostModel.objects.filter(~Q(author__in=user_blocked)),
            
        }
        return render(request,'home/home.html',context=context)

    def post(self,request):
        pass

class AddPostView(generic.CreateView):
    form_class = AddPostForm
    template_name = 'home/add-post.html'


    def form_valid(self,form):
        post_form = form.save(commit=False)
        if self.request.FILES:
            file = self.request.FILES['file']

            if "audio" in file.content_type:
                post_form.audio = file
            if "video" in file.content_type:
                post_form.video = file
            if "image" in file.content_type:
                post_form.image = file

        post_form.author = self.request.user
        post_form.slug = slugify(form.cleaned_data['title'])
        post_form.status = 'p'
        post_form.save()
        return HttpResponseRedirect('/')



class DeletePostView(AuthorAccessMixin,generic.DeleteView):
    template_name = 'home/delete-post.html'
    model = PostModel
    success_url = reverse_lazy('home:home')



class UpdatePostView(AuthorAccessMixin,generic.UpdateView):
    template_name = 'home/edit-post.html'
    model = PostModel
    fields = ('title',)
    success_url = reverse_lazy('home:home')



class CommentPostView(LoginRequiredMixin,View):
    template_name = 'home/comments.html'
    def get(self,request,username,slug,pk):
        #post
        post = PostModel.objects.get(slug=slug)
        #comment
        comment = CommentModel.objects.filter(post=post,status='A')
        #form comment
        cm_form = CommentForm(request.POST)

        context = {
        'comments':comment,'post':post,
        'total_comments':comment.count(),'form':cm_form,
        }
        return render(request,self.template_name,context)


    def post(self,request,username,slug,pk):
        post = PostModel.objects.get(slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid:
            cm_form = form.save(commit=False)
            cm_form.from_user = request.user
            cm_form.to_user = post.author
            cm_form.post = post
            cm_form.status = 'i'
            cm_form.save()
            return redirect('home:comment',username,slug,pk)




class MessagesProfileView(LoginRequiredMixin,View):
    def get(self,request):
        comments = CommentModel.objects.filter(Q(to_user = request.user) & Q(status = 'i'))
        post_count = PostModel.objects.filter(author=request.user).count()
        uploaded_file_count = PostModel.objects.filter(~Q(video=None) & ~Q(image=None) & ~Q(audio=None) & Q(author=request.user)).count()
        comment_count =CommentModel.objects.filter(to_user = request.user).count()


        context = {
            'comments':comments,
            'post_count':post_count,
            'comment_count':comment_count,
            'uploaded_file_count':uploaded_file_count,
        }
        
        return render(request,'home/messages.html',context)
    def post(self,request): 
        pass


class AcceptCommentView(SuperUserAuthorAccessMixin,LoginRequiredMixin,View):
    def get(self, request,pk):
        cm = CommentModel.objects.filter(pk=pk)
        cm.update(status='A')
        return redirect('home:messages')




class ReportPostView(View):
    template_name = 'home/report-post.html'
    form_class = ReportPostForm
    def get(self,request,author,slug):
        form = self.form_class
        return render(request,self.template_name,{'form':form})
    def post(self,request,author,slug):
        from_user = User.objects.get(username = request.user.username)
        to_user = User.objects.get(username=author)
        post = PostModel.objects.get(slug=slug)
        form=self.form_class(request.POST)
        if form.is_valid():
            report_text = form.cleaned_data['report_text']
            ReportPostModel.objects.create(from_user=from_user,to_user=to_user,post=post,report_text=report_text)
            messages.success(request,"Thank's For Report")
            return redirect('home:home')
        return redirect('home:home')
        