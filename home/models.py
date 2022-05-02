from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class CategoryModel(models.Model):
    parent = models.ForeignKey('self',default=None,null=True,blank=True,on_delete=models.SET_NULL,related_name='children')
    name = models.CharField(max_length=100)
    slug  = models.SlugField(max_length=100)   
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    




class PostModel(models.Model):
    Status = (
        ('p','Published'),
        ('d','Draft'),
        ('i','Investigation'),
        ('b','Back'),

    )
    author= models.ForeignKey(User,on_delete=models.CASCADE,related_name='writer')
    title = models.CharField(max_length=150)
    slug  = models.SlugField(max_length=150)
    image = models.ImageField(upload_to = 'images/%Y/%m/%d/')
    video = models.FileField(upload_to= 'video/%Y/%m/%d/')
    audio = models.FileField(upload_to='audio/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=Status)


    def __str__(self):
        return f"{self.author} - {self.title[:10]}"