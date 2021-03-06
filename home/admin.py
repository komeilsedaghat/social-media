from django.contrib import admin
from .models import PostModel,CategoryModel,IPAdressModel,CommentModel,ReportPostModel
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','created','status')
    prepopulated_fields = {"slug": ("title",)}
    list_filter  = ('status','author')
    search_fields = ('title',)

admin.site.register(PostModel,PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent','status')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('status',)
    search_field = ('title',)

admin.site.register(CategoryModel,CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('from_user','comment','status')
    list_filter = ('status','from_user')
    search_field = ('comment',)

admin.site.register(CommentModel,CommentAdmin)




class IPAdressAdmin(admin.ModelAdmin):
    list_display = ('user','IP_Address')

admin.site.register(IPAdressModel,IPAdressAdmin)


class ReportPostAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user','report_text')
    list_filter = ('from_user','to_user','post','created',)

admin.site.register(ReportPostModel,ReportPostAdmin)