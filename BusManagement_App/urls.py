from django.urls import path
from . import views
from .views import user_login 
from .views import user_logout
from .views import parent_dashboard

urlpatterns = [
    # Your app's url patterns
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/parent/', parent_dashboard, name='parent_dashboard'),
  
]

    # ... other patterns for BusManagement_App

