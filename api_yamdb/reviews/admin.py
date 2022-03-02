from django.contrib import admin

from .models import Comment, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'genre',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'score',
        'created',
        'author',
        'titles'
    )
    search_fields = ('text', 'created', 'author', 'score')
    list_filter = ('created', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'reviews',
        'author',
        'text',
        'created'
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
