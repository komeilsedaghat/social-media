from django.contrib import admin
from .models import PostModel,CategoryModel
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('title','author','created','status')
    prepopulated_fields = {"slug": ("title",)}
    list_filter  = ('status','author')
    search_fields = ('title',)

admin.site.register(PostModel,PostAdmin)