from django.contrib import admin
from BusManagement_App.models import Bus, Driver, Route,Student, Admin,SecondaryAddressRequest,SafetyCheck,Schedule,Tarif

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

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ['route', 'montant']  # Affichez les champs que vous souhaitez voir dans l'interface d'administration
    search_fields = ['route__name']  # Permettez la recherche par nom de route

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['route', 'departure_time', 'arrival_time']
    list_filter = ['route']  # Filtrez par route dans l'interface d'administration

@admin.register(SafetyCheck)
class SafetyCheckAdmin(admin.ModelAdmin):
    list_display = ['bus', 'check_date', 'is_passed']
    list_filter = ['is_passed', 'check_date']
    search_fields = ['bus__number']

@admin.register(SecondaryAddressRequest)
class SecondaryAddressRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'address', 'is_approved']
    list_filter = ['is_approved']
    search_fields = ['student__first_name', 'student__last_name', 'address']

   

# Enregistrement des modèles avec les classes d'administration personnalisées
admin.site.register(Bus, BusAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
