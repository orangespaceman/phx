from django.contrib import admin

from phx.admin import phx_admin

from .models import Event


class EventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'date']
    exclude = ['uploaded_by']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


phx_admin.register(Event, EventsAdmin)
