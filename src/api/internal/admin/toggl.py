from api.internal.models.toggl import TogglRecord
from django.contrib import admin


@admin.register(TogglRecord)
class TogglDataAdmin(admin.ModelAdmin):
    list_display = ('start', 'employee', 'rate', 'project', 'seconds')
    list_display_links = ('start', 'employee', 'rate', 'project', 'seconds')
    readonly_fields = ('start', 'employee', 'project', 'seconds')
    list_filter = ('start', 'employee__username', 'project')
