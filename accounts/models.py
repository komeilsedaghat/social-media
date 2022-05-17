from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.

class User(AbstractUser):
    regex = RegexValidator(regex="(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}", 
    message="Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed.")
    phone_number = models.CharField(max_length=11,validators=[regex],unique=True)
    age = models.PositiveSmallIntegerField(null=True,blank=True)
    profile_img = models.ImageField(upload_to='users/pics/',blank=True)
    TFA = models.BooleanField(default=False)
    blocked_users = models.ManyToManyField('self', symmetrical=False,related_name='blocked',blank=True)


class OtpCode(models.Model):
    email = models.EmailField()
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.email} - {self.code} - {self.created}"


class FollowUserModel(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow_from_user',null=True)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow_to_user',null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}"
        