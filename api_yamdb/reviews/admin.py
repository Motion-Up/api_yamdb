from django.contrib import admin

from .models import Comment, Review, Title, Genre, Category


class TitleAdmin(admin.ModelAdmin):
    def genres(self, obj):
        all_genres = obj.genre.all()
        return [genre for genre in all_genres]

    list_display = (
        'name',
        'genres',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'rating',
        'created',
        'author',
        'title'
    )
    search_fields = ('text', 'created', 'author', 'rating')
    list_filter = ('created', 'rating')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'created'
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
