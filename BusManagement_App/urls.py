from django.urls import path
from . import views
from .views import user_login 
from .views import user_logout

urlpatterns = [
    # Your app's url patterns
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
  
]

    # ... other patterns for BusManagement_App

