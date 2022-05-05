from .forms import ProfileUserForm
from django.http import Http404
from django.contrib.auth import get_user_model

User = get_user_model()


class FieldMixin():
    def dispatch(self,request,*args,**kwargs):
        def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            username = self.kwargs.get('username')
            context['user'] = User.objects.get(username=username)
            return context

        return super().dispatch(request,*args,**kwargs)
