from django.db import models


class IsPublishedCreatedAt(models.Model):
    """Абстрактная модель для модели публикации.

    Содержит в себе поля разрешения на публикацию и дату создания.
    """

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
