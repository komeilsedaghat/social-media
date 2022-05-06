from django.http import Http404

class AuthorAccessMixin():
    def dispatch(self,request,*args,**kwargs):
        username = kwargs.get('username')
        if request.user.username == username:
            return super().dispatch(request,*args,**kwargs)
        else:
            raise Http404