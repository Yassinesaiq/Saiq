from django.contrib import admin
from BusManagement_App.models import Bus, Driver, Route,Student,Parent, Admin,SecondaryAddressRequest,SafetyCheck,Schedule,Tarif,Notification
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'model','photo')
    search_fields = ('number', 'model')

class DriverAdmin(admin.ModelAdmin):
    list_display = ('get_username','first_name', 'last_name','Sex', 'license_number', 'bus')
    list_filter = ('bus',)
    search_fields = ('user__username','first_name', 'last_name', 'license_number')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group = Group.objects.get(name='Conducteurs')  # Assurez-vous que ce groupe existe
        group.user_set.add(obj.user)  # 

    def get_username(self, obj):
     return obj.user.username if obj.user else 'No user'
    
    


class RouteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', #'start_point', 'end_point'
                           )}),
        ('Buses', {'fields': ('buses',), 'description': 'Select buses for this route'}),
    )
    filter_horizontal = ('buses',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','Sex', 'grade','is_eligible_for_transport')
    list_filter = ('grade','is_eligible_for_transport')
    search_fields = ('first_name', 'last_name', 'grade')

    def save_model(self, request, obj, form, change):
        
        if obj.parent:
            other_students = Student.objects.filter(parent=obj.parent).exclude(id=obj.id)
            for student in other_students:
                if student.address != obj.address:
                    raise ValidationError("L'adresse ne peut pas être différente pour les étudiants ayant le même parent.")

        DISTANCE_CRITERIA_GENERAL = 3  # Tous les élèves à 3km ou plus sont éligibles
        DISTANCE_CRITERIA = {
            'PS4': 0,  # Préscolaire 4 ans toujours éligible
            'PS5': 0.8,  # Préscolaire 5 ans à 0.8 km ou plus
            # Ajouter des critères pour les niveaux primaire et secondaire
            'CP': 1.6, 'CE1': 1.6, 'CE2': 1.6, 'CM1': 1.6, 'CM2': 1.6,  # Primaire
            '6E': 1.6, '5E': 1.6, '4E': 1.6, '3E': 1.6,  # Collège
            '2ND': 1.6, '1RE': 1.6, 'TLE': 1.6,  # Lycée
        }

        if obj.has_special_needs or obj.temporary_disability:
            obj.is_eligible_for_transport = True
        elif obj.distance_to_school >= DISTANCE_CRITERIA_GENERAL:
            obj.is_eligible_for_transport = True
        elif obj.grade in DISTANCE_CRITERIA and obj.distance_to_school >= DISTANCE_CRITERIA[obj.grade]:
            obj.is_eligible_for_transport = True
        else:
            obj.is_eligible_for_transport = False

        super().save_model(request, obj, form, change)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title')
    search_fields = ('user__first_name', 'user__last_name', 'job_title')

class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'first_name', 'last_name','Sex', 'cnie',)
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'cnie',)

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Permet le tri sur le nom d'utilisateur
    get_username.short_description = 'Nom d’utilisateur'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'  # Permet le tri sur l'email
    get_email.short_description = 'Email'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group = Group.objects.get(name='Parents')  # Assurez-vous que ce groupe existe
        group.user_set.add(obj.user)  # 



class TarifAdmin(admin.ModelAdmin):
    list_display = ['route', 'montant']  # Affichez les champs que vous souhaitez voir dans l'interface d'administration
    search_fields = ['route__name']  # Permettez la recherche par nom de route

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['route', 'departure_time', 'arrival_time']
    list_filter = ['route']  # Filtrez par route dans l'interface d'administration


class SafetyCheckAdmin(admin.ModelAdmin):
    list_display = ['student','bus', 'check_date', 'is_passed']
    list_filter = ['is_passed', 'check_date']
    search_fields = ['bus__number']


class SecondaryAddressRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'address', 'is_approved']
    list_filter = ['is_approved']
    search_fields = ['student__first_name', 'student__last_name', 'address']

class NotificationAdmin(admin.ModelAdmin):
    list_display=['student_id','message','created_at']
   

# Enregistrement des modèles avec les classes d'administration personnalisées
admin.site.register(Bus, BusAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Schedule)
admin.site.register(SecondaryAddressRequest, SecondaryAddressRequestAdmin)
admin.site.register(SafetyCheck,SafetyCheckAdmin)
admin.site.register(Notification,NotificationAdmin)


from django.contrib import admin
from .models import GeocodedAddress

admin.site.register(GeocodedAddress)