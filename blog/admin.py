from django.contrib import admin
from .models import Articles, Pages, Comment

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id","title", "slug","status","published")

class PagesAdmin(admin.ModelAdmin):
    list_display = ("title","slug")
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'articles', 'created','body','active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

admin.site.register(Articles,ArticleAdmin)
admin.site.register(Pages,PagesAdmin)
