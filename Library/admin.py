from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from Library.models import User, Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'isbn',
        'publisher',
        'publication_date',
        'genre',
        'language',
        'pages',
        'price',
        'quantity_in_stock'
    ]
    search_fields = ['title', 'author', 'isbn', 'publisher', 'genre', 'language']
    list_filter = ['genre', 'language', 'publication_date']
    ordering = ['id']


class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "role", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "role"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "role", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


admin.site.register(User, UserModelAdmin)
