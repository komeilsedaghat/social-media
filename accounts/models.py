from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.

class User(AbstractUser):
    regex = RegexValidator(regex="(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}", 
    message="Phone number must be entered in the format: '+999999999'. Up to 11 digits allowed.")
    phone_number = models.CharField(max_length=11,validators=[regex],unique=True)
    age = models.PositiveSmallIntegerField(null=True,blank=True)
