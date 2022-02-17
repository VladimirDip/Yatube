from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    list_editable = ("group",)



class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "created")
    search_fields = ("text",)
    list_filter = ("created",)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

