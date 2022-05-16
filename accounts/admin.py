from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import OtpCode
# Register your models here.

User = get_user_model()

UserAdmin.fieldsets[1][1]['fields'] = (
                        'first_name',
                        'last_name',
                        'profile_img',
                        'email',
                        'phone_number',
                        'TFA',
                        'blocked_users',
)

UserAdmin.list_display += (
    'phone_number',
)

admin.site.register(User,UserAdmin)


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('email','code','created')

admin.site.register(OtpCode,OtpCodeAdmin)