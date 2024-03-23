
from django.contrib import admin
from django.urls import path, include, re_path
from BusManagement_App import views
from rest_framework.routers import DefaultRouter
from BusManagement_App.views import SignupView 


router = DefaultRouter()
router.register(r'buses', views.BusViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'admins', views.AdminViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('BusManagement_App/', include('BusManagement_App.urls')),
    # URLs pour les Bus
    path('buses/', views.BusListView.as_view(), name='bus_list'),
    path('bus/<int:pk>/', views.BusDetailView.as_view(), name='bus_detail'),
    path('bus/add/', views.BusCreateView.as_view(), name='bus_add'),
    path('bus/<int:pk>/edit/', views.BusUpdateView.as_view(), name='bus_edit'),
    path('bus/<int:pk>/delete/', views.BusDeleteView.as_view(), name='bus_delete'),


   
    path('parent/modifier/<int:parent_id>/', views.modifier_parent, name='modifier_parent'),
     path('parent/supprimer/<int:parent_id>/', views.supprimer_parent, name='supprimer_parent'),

    # URLs pour les Conducteurs

    path('drivers/', views.DriverListView.as_view(), name='driver_list'),
    path('driver/<int:pk>/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('driver/add/', views.DriverCreateView.as_view(), name='driver_add'),
    path('driver/<int:pk>/edit/', views.DriverUpdateView.as_view(), name='driver_edit'),
    path('driver/<int:pk>/delete/', views.DriverDeleteView.as_view(), name='driver_delete'),

    # URLs pour les Routes
    path('routes/', views.RouteListView.as_view(), name='route_list'),
    path('route/<int:pk>/', views.RouteDetailView.as_view(), name='route_detail'),
    path('route/add/', views.RouteCreateView.as_view(), name='route_add'),
    path('route/<int:pk>/edit/', views.RouteUpdateView.as_view(), name='route_edit'),
    path('route/<int:pk>/delete/', views.RouteDeleteView.as_view(), name='route_delete'),


    # URLs pour les Étudiants
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('student/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # URLs pour les Administrateurs
    path('admins/', views.AdminListView.as_view(), name='admin_list'),
    path('admin/<int:pk>/', views.AdminDetailView.as_view(), name='admin_detail'),
    path('admin/add/', views.AdminCreateView.as_view(), name='admin_add'),
    path('admin/<int:pk>/edit/', views.AdminUpdateView.as_view(), name='admin_edit'),
    path('admin/<int:pk>/delete/', views.AdminDeleteView.as_view(), name='admin_delete'),

]
