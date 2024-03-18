from django.contrib import admin

from .constants import LENGTH_STRING_ADMIN
from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Post."""

    list_display = (
        'title',
        'text_short',
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
        'location',
    )
    list_per_page = 10

    @staticmethod
    @admin.display(description='Текст')
    def text_short(obj: Post) -> str:
        """Укороченное описание поста для отображения в админке."""
        return f'{obj.text[:LENGTH_STRING_ADMIN]}...'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Category."""

    list_display = (
        'title',
        'description_short',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'slug',
    )
    list_filter = (
        'title',
        'description',
    )
    list_per_page = 10

    @staticmethod
    @admin.display(description='Описание')
    def description_short(obj: Category) -> str:
        """Укороченное названия категории для отображения в админке."""
        return f'{obj.description[:LENGTH_STRING_ADMIN]}...'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Location."""

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    list_filter = ('name',)
    list_per_page = 10
