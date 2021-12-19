from django.contrib import admin
from .models import Post, SharePost, Comment



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'file_field', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'file',]



@admin.register(SharePost)
class SharePostAdmin(admin.ModelAdmin):
    list_display = ['file', 'user', 'sharedUser']