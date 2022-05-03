from django.shortcuts import render
from django.views import View
from .models import PostModel
# Create your views here.


class HomeView(View):
    def get(self,request):
        context = {
            'posts':PostModel.objects.publish()
        }
        return render(request,'home/home.html',context=context)

    def post(self,request):
        pass 