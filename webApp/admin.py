from django.contrib import admin
from .models import *


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slug', 'is_active', 'is_trending', 'created_at')
    list_editable = ('slug','is_active', 'is_trending',)
    list_filter = ('created_at',)
    list_per_page = 10
    search_fields = ('title',)



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slug', 'image', 'created_at')
    list_editable = ('slug', 'image')
    list_filter = ('tag','category',)
    list_per_page = 10
    search_fields = ('title','tag',)
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slug', 'is_active', 'is_trending', 'created_at')
    list_editable = ('slug', 'is_active', 'is_trending')
    list_filter = ('created_at',)
    list_per_page = 10
    search_fields = ('title',)
    

@admin.register(MainBlog)
class MainBlogAdmin(admin.ModelAdmin):
    list_display  = ('blog', 'is_active')
    list_editable = ('is_active',)
    
    
    
@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display  = ('email',)



@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'comment')
    list_filter = ('user',)
    list_per_page = 10
    
    
    
@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display  = ('id','reply', 'parent', 'user')
    list_filter = ('user', 'parent',)
    list_per_page = 10
    