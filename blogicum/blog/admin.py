from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .constants import LENGTH_STRING_ADMIN, NUMBER_OF_POSTS
from .models import Category, Comment, Location, Post


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
        'image_display',
        'author_display',
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
    list_per_page = NUMBER_OF_POSTS

    @admin.display(description='Картинка')
    def image_display(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )

    @staticmethod
    @admin.display(description='Текст')
    def text_short(obj: Post) -> str:
        """Укороченное описание поста для отображения в админке."""
        return f'{obj.text[:LENGTH_STRING_ADMIN]}...'

    @admin.display(description='Автор')
    def author_display(self, obj):
        link = reverse(
            'admin:auth_user_change', args=(obj.author.id,)
        )
        return format_html(
            '<a href="{}">{}</a>', link, obj.author.get_full_name()
        )


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
    list_per_page = NUMBER_OF_POSTS

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
    list_per_page = NUMBER_OF_POSTS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Comment."""

    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )
    list_filter = ('text',)
    list_per_page = NUMBER_OF_POSTS
