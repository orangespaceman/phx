from django.contrib import admin

from phx.admin import phx_admin

from .models import Category, Fixture


class FixtureAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'event_date',
        'age_groups',
        'location',
        'author',
    ]
    ordering = ['-event_date']
    exclude = ['author']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'abbreviation']
    pass


phx_admin.register(Category, CategoryAdmin)
phx_admin.register(Fixture, FixtureAdmin)
