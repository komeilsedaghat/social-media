from builtins import print
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import CommentModel, PostModel,CategoryModel
from django.views import generic
from .forms import AddPostForm, CommentForm
from django.contrib.auth import get_user_model
from .mixins import AuthorAccessMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

User = get_user_model()


class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'posts':PostModel.objects.publish()
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
            cm_form.user = request.user
            cm_form.post = post
            cm_form.status = 'i'
            cm_form.save()
            return redirect('home:comment',username,slug,pk)




class MessagesProfileView(View):
    def get(self,request):
        pass 
    def post(self,request):
        pass