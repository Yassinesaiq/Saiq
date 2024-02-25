from django.urls import path
from . import views
from .views import user_login 
from .views import user_logout
from .views import SafetyCheckCreateView,SafetyCheckUpdateView,SafetyCheckDeleteView, SafetyCheckListView ,SecondaryAddressRequestListView,SecondaryAddressRequestCreateView,SecondaryAddressRequestDeleteView,SecondaryAddressRequestUpdateView
from .views import TarifDeleteView,TarifUpdateView,TarifListView,TarifCreateView,ScheduleListView,ScheduleCreateView,ScheduleUpdateView,ScheduleDeleteView
urlpatterns = [
    # Your app's url patterns
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('login/parent/', views.login_parent, name='login_parent'),
    path('login/director/', views.login_director, name='login_director'),
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



]

    # ... other patterns for BusManagement_App

