from django.contrib import admin

from .models import Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'genre',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)