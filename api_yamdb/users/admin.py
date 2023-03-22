from django.contrib import admin

from users.models import User
from reviews.models import Title, Review, Categories


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )
    list_editable = (
        'role',
    )
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'score',
        'pub_date',
        'title',
    )
    empty_value_display = '-пусто-'


@admin.register(Categories)
class Categories(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
