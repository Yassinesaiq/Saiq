from django.contrib import admin
from BusManagement_App.models import Bus, Driver, Route,Student, Admin

class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'model')
    search_fields = ('number', 'model')

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license_number', 'bus')
    list_filter = ('bus',)
    search_fields = ('first_name', 'last_name', 'license_number')

class RouteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'start_point', 'end_point')}),
        ('Buses', {'fields': ('buses',), 'description': 'Select buses for this route'}),
    )
    filter_horizontal = ('buses',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade')
    list_filter = ('grade',)
    search_fields = ('first_name', 'last_name', 'grade')

class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title')
    search_fields = ('user__first_name', 'user__last_name', 'job_title')

# Enregistrement des modèles avec les classes d'administration personnalisées
admin.site.register(Bus, BusAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
