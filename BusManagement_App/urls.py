from django.urls import path,include
from . import views
from .views import user_logout,login_user
from .views import SafetyCheckCreateView,SafetyCheckUpdateView,SafetyCheckDeleteView, SafetyCheckListView ,SecondaryAddressRequestListView,SecondaryAddressRequestCreateView,SecondaryAddressRequestDeleteView,SecondaryAddressRequestUpdateView
from .views import TarifDeleteView,TarifUpdateView,TarifListView,TarifCreateView,ScheduleListView,ScheduleCreateView,ScheduleUpdateView,ScheduleDeleteView
from .views import StudentListView, StudentCreateView, StudentDetailView, StudentUpdateView, StudentDeleteView
from .views import parent_add, parent_edit, parent_detail, parent_delete,profil_parent,update_parent_email
from .views import modifier_parent, supprimer_parent
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from .views import get_geojson_data, my_view




router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    # Your app's url patterns

    path('api/geojson-data/', get_geojson_data, name='get_geojson_data'),


    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', user_logout, name='logout'),
    path('login/', login_user, name='login_user'),
    path('home/', views.home, name='home'),
    path('dashboard/director/', views.director_dashboard, name='director_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('ajouter_parent/', views.ajouter_parent, name='ajouter_parent'),
    path('parent/modifier/<int:parent_id>/', modifier_parent, name='modifier_parent'),
    path('parent/supprimer/<int:parent_id>/', supprimer_parent, name='supprimer_parent'),
    path('ajouter_bus/', views.ajouter_bus, name='ajouter_bus'),
    path('ajouter_chauffeur/', views.ajouter_chauffeur, name='ajouter_chauffeur'),

# Pour SafetyCheck
    path('safetychecks/add/', SafetyCheckCreateView.as_view(), name='add_safety_check'),
    path('safetychecks/', SafetyCheckListView.as_view(), name='list_safety_checks'), 
    path('safetychecks/<int:pk>/update/', SafetyCheckUpdateView.as_view(), name='update_safety_check'),
    path('safetychecks/<int:pk>/delete/', SafetyCheckDeleteView.as_view(), name='delete_safety_check'),

# Pour SecondaryAddressRequest
    path('secondary-address-requests/add/', SecondaryAddressRequestCreateView.as_view(), name='add_secondary_address_request'),
    path('secondary-address-requests/', SecondaryAddressRequestListView.as_view(), name='list_secondary_address_requests'),
    path('secondary-address-requests/<int:pk>/update/', SecondaryAddressRequestUpdateView.as_view(), name='update_secondary_address_request'),
    path('secondary-address-requests/<int:pk>/delete/', SecondaryAddressRequestDeleteView.as_view(), name='delete_secondary_address_request'),

    path('schedules/add/', ScheduleCreateView.as_view(), name='add_schedule'),
    path('list_schedules/', ScheduleListView.as_view(), name='list_schedules'),
    path('schedules/<int:pk>/update/', ScheduleUpdateView.as_view(), name='update_schedule'),
    path('schedules/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='delete_schedule'),
    
    # URLs pour Tarif
    path('tarifs/add/', TarifCreateView.as_view(), name='add_tarif'),
    path('tarifs/', TarifListView.as_view(), name='list_tarifs'),
    path('tarifs/<int:pk>/update/', TarifUpdateView.as_view(), name='update_tarif'),
    path('tarifs/<int:pk>/delete/', TarifDeleteView.as_view(), name='delete_tarif'),

    # URLs pour Students
    path('', include(router.urls)),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/add/', StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    # ... your other URL patterns

    path('parent/add/', parent_add, name='parent_add'),
    path('parent/<int:pk>/edit/', parent_edit, name='parent_edit'),
    path('parent/<int:pk>/', parent_detail, name='parent_detail'),
    path('parent/<int:pk>/delete/', parent_delete, name='parent_delete'),
    path('profil_parent/', profil_parent, name='profil_parent'),
    path('parent/update_email/', update_parent_email, name='update_parent_email'),


    path('api/routes/', views.get_routes_api, name='api_routes'),
    path('map/', views.my_view, name='map'),
    path('update_address/', views.update_address, name='update_address'),

 

    
  




]+ router.urls

    # ... other patterns for BusManagement_App

