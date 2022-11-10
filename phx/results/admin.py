from django.contrib import admin

from phx.admin import phx_admin

from .models import Result


class ResultAdmin(admin.ModelAdmin):
    # display data on results listing view
    list_display = ['title', 'event_date', 'author']

    # order list display view by event date
    def get_queryset(self, request):
        qs = super(ResultAdmin,
                   self).get_queryset(request).order_by('-event_date')
        return qs

    def get_exclude(self, request, obj):
        return ['author']

    def get_readonly_fields(self, request, obj):
        return []

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


phx_admin.register(Result, ResultAdmin)
