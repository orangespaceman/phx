from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field
from import_export.widgets import DateWidget, Widget

from phx.admin import phx_admin

from .models import Event, Performance, Result


@admin.action(description="Publish selected results")
def publish_results(_modeladmin, request, queryset):
    queryset.filter(draft=True).update(draft=False, author=request.user)


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
    actions = [publish_results]

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


class GenderWidget(Widget):

    def render(self, value, obj=None):
        if value == 'W':
            return 'Female'

        if value == 'M':
            return 'Male'

        return ''


class PerformanceResource(resources.ModelResource):
    athlete__first_name = Field(attribute='athlete__first_name',
                                column_name='First Name')
    athlete__last_name = Field(attribute='athlete__last_name',
                               column_name='Last Name')
    distance = Field(attribute='distance', column_name='Event Distance')
    overall_position = Field(attribute='overall_position',
                             column_name='Position')
    athlete__age_category = Field(attribute='athlete__age_category',
                                  column_name='Age Category')
    date = Field(attribute='date',
                 column_name='Event Date',
                 widget=DateWidget('%d/%m/%Y'))
    athlete__gender = Field(attribute='athlete__gender',
                            column_name='Sex',
                            widget=GenderWidget())
    age_position = Field(attribute='age_position',
                         column_name='Age Category Position')
    gender_position = Field(attribute='gender_position',
                            column_name='Gender Position')
    event__name = Field(attribute='event__name', column_name='Event Name')
    time = Field(attribute='time', column_name='Time')

    class Meta:
        model = Performance
        fields = (
            'athlete__first_name',
            'athlete__last_name',
            'distance',
            'overall_position',
            'athlete__age_category',
            'date',
            'athlete__gender',
            'age_position',
            'gender_position',
            'event__name',
            'time',
        )


class PerformancesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['athlete', 'event', 'date', 'distance', 'time']
    exclude = ['uploaded_by']
    resource_classes = [PerformanceResource]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'uploaded_by', None) is None:
            obj.uploaded_by = request.user
        obj.save()


phx_admin.register(Performance, PerformancesAdmin)
phx_admin.register(Result, ResultAdmin)
phx_admin.register(Event, EventsAdmin)
