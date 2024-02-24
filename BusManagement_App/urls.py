from django.urls import path
from . import views
from .views import user_login 
from .views import user_logout


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
]

    # ... other patterns for BusManagement_App

