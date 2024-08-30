from django.contrib import admin

from phx.admin import phx_admin

from .models import Event, Performance, Result


class EventInline(admin.StackedInline):
    """
    A readonly InlineModelAdmin used to show related
    Events from within the Result admin interface
    """

    model = Event
    extra = 0
    can_delete = False
    fields = ['date']
    readonly_fields = ['date']

    def has_add_permission(self, request, obj):
        return False


class ResultAdmin(admin.ModelAdmin):
    # display data on results listing view
    list_display = ['title', 'event_date', 'author', 'published']
    ordering = ['-created_date']
    search_fields = ['title']
    inlines = [EventInline]

    # order list display view by event date
    def get_queryset(self, request):
        qs = super(ResultAdmin,
                   self).get_queryset(request).order_by('-event_date')
        return qs

    def get_exclude(self, request, obj):
        return ['author']

    def get_readonly_fields(self, request, obj):
        return []

    @admin.display(boolean=True)
    def published(self, obj):
        return not obj.draft

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class EventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'date']
    exclude = ['uploaded_by']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


class PerformancesAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'event', 'distance', 'time']
    exclude = ['uploaded_by']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


phx_admin.register(Performance, PerformancesAdmin)
phx_admin.register(Result, ResultAdmin)
phx_admin.register(Event, EventsAdmin)
