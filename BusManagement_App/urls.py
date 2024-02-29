from django.urls import path
from . import views
from .views import user_logout,login_user
from .views import SafetyCheckCreateView,SafetyCheckUpdateView,SafetyCheckDeleteView, SafetyCheckListView ,SecondaryAddressRequestListView,SecondaryAddressRequestCreateView,SecondaryAddressRequestDeleteView,SecondaryAddressRequestUpdateView
from .views import TarifDeleteView,TarifUpdateView,TarifListView,TarifCreateView,ScheduleListView,ScheduleCreateView,ScheduleUpdateView,ScheduleDeleteView
from .views import StudentListView, StudentCreateView, StudentDetailView, StudentUpdateView, StudentDeleteView
from .views import parent_add, parent_edit, parent_detail, parent_delete

urlpatterns = [
    # Your app's url patterns
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', user_logout, name='logout'),
    path('login/', login_user, name='login_user'),
    path('home/', views.home, name='home'),
    path('dashboard/director/', views.director_dashboard, name='director_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('ajouter_parent/', views.ajouter_parent, name='ajouter_parent'),
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
    path('schedules/', ScheduleListView.as_view(), name='list_schedules'),
    path('schedules/<int:pk>/update/', ScheduleUpdateView.as_view(), name='update_schedule'),
    path('schedules/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='delete_schedule'),
    
    # URLs pour Tarif
    path('tarifs/add/', TarifCreateView.as_view(), name='add_tarif'),
    path('tarifs/', TarifListView.as_view(), name='list_tarifs'),
    path('tarifs/<int:pk>/update/', TarifUpdateView.as_view(), name='update_tarif'),
    path('tarifs/<int:pk>/delete/', TarifDeleteView.as_view(), name='delete_tarif'),

    # URLs pour Students
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



]

    # ... other patterns for BusManagement_App

