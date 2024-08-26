from django.contrib import admin

from phx.admin import phx_admin

from .models import Performance


class PerformancesAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'event', 'distance', 'time']
    exclude = ['uploaded_by']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


phx_admin.register(Performance, PerformancesAdmin)
