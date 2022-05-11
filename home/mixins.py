from django.http import Http404

from home.models import CommentModel

class AuthorAccessMixin():
    def dispatch(self,request,*args,**kwargs):
        username = kwargs.get('username')
        if request.user.username == username:
            return super().dispatch(request,*args,**kwargs)
        else:
            raise Http404



class SuperUserAuthorAccessMixin():
    def dispatch(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        cm = CommentModel.objects.get(pk=pk)
        if request.user.is_superuser or request.user == cm.post.author:
            return super().dispatch(request,*args,**kwargs)
        else:
            raise Http404
