from django.contrib import admin

# Register your models here.
from .models import Post , Author , Tag,Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
    list_filter = ("author", "tags", "date")
    list_display = ("title", "date", "author")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post")

admin.site.register(Post , PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment , CommentAdmin)
