from django.contrib import admin
from BusManagement_App.models import Bus, Driver, Route,Student,Parent, Admin,SecondaryAddressRequest,SafetyCheck,Schedule,Tarif


class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'model')
    search_fields = ('number', 'model')

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license_number', 'bus')
    list_filter = ('bus',)
    search_fields = ('first_name', 'last_name', 'license_number')

class RouteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', #'start_point', 'end_point'
                           )}),
        ('Buses', {'fields': ('buses',), 'description': 'Select buses for this route'}),
    )
    filter_horizontal = ('buses',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade','is_eligible_for_transport')
    list_filter = ('grade','is_eligible_for_transport')
    search_fields = ('first_name', 'last_name', 'grade')

class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title')
    search_fields = ('user__first_name', 'user__last_name', 'job_title')

class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'first_name', 'last_name', 'cnie',)
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'cnie',)

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Permet le tri sur le nom d'utilisateur
    get_username.short_description = 'Nom d’utilisateur'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'  # Permet le tri sur l'email
    get_email.short_description = 'Email'



class TarifAdmin(admin.ModelAdmin):
    list_display = ['route', 'montant']  # Affichez les champs que vous souhaitez voir dans l'interface d'administration
    search_fields = ['route__name']  # Permettez la recherche par nom de route

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['route', 'departure_time', 'arrival_time']
    list_filter = ['route']  # Filtrez par route dans l'interface d'administration


class SafetyCheckAdmin(admin.ModelAdmin):
    list_display = ['bus', 'check_date', 'is_passed']
    list_filter = ['is_passed', 'check_date']
    search_fields = ['bus__number']


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
admin.site.register(Parent, ParentAdmin)
admin.site.register(Schedule)
admin.site.register(SecondaryAddressRequest, SecondaryAddressRequestAdmin)


from django.contrib import admin
from .models import GeocodedAddress

admin.site.register(GeocodedAddress)