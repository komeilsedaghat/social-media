from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError

User = get_user_model()


#Category Manager
class CategoryManager(models.Manager):
    def publish(self):
        return self.filter(status = True)

#Category Model
class CategoryModel(models.Model):
    parent = models.ForeignKey('self',default=None,null=True,blank=True,on_delete=models.SET_NULL,related_name='children')
    name = models.CharField(max_length=100)
    slug  = models.SlugField(max_length=100)   
    status = models.BooleanField(default=True)
    objects = CategoryManager()

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name




#Post Manager
class PostManager(models.Manager):
    def publish(self):
        return self.filter(status = 'p')
    
    def draft(self):
        return self.filter(status = 'd')
    
    def investigation(self):
        return self.filter(status = 'i')

    def back(self):
        return self.filter(status = 'b')


#validator for uploaded file
def Uploaded_size(value):
    max_size = 104857600
    if value.size > max_size:
        raise ValidationError('You Uploaded File Must Be Less Then 100MB')
        

#Post Model
class PostModel(models.Model):
    post_status = (
        ('p','Published'),
        ('d','Draft'),
        ('i','Investigation'),
        ('b','Back'),

    )
    author= models.ForeignKey(User,on_delete=models.CASCADE,related_name='writer')
    title = models.CharField(max_length=150)
    slug  = models.SlugField(max_length=150)
    image = models.ImageField(upload_to = 'images/%Y/%m/%d/',blank=True,validators = [Uploaded_size])
    video = models.FileField(upload_to= 'video/%Y/%m/%d/',blank=True,validators = [Uploaded_size])
    audio = models.FileField(upload_to='audio/%Y/%m/%d/',blank=True,validators = [Uploaded_size])
    category = models.ManyToManyField(CategoryModel,related_name='category')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=post_status)
    objects = PostManager()


    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-created',)


    def __str__(self):
        return f"{self.author} - {self.title[:10]}"



class CommentModel(models.Model):
    cm_status = (
        ('A','Accepted'),
        ('i','Investigation'),
        ('R','Rejected'),
    )
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="from_user") 
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="to_user")
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE,null=True,related_name='post')
    comment = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=cm_status)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.from_user} - {self.comment}"


class IPAdressModel(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    IP_Address = models.GenericIPAddressField(null=True)


    def __str__(self):
        return self.IP_Address



