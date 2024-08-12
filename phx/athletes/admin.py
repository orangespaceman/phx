from django.contrib import admin

from phx.admin import phx_admin

from .models import Athlete


class AthleteAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'age_category']
    exclude = ['uploaded_by']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


phx_admin.register(Athlete, AthleteAdmin)
