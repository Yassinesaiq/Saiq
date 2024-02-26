from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Bus, Driver, Route, Student, Admin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import viewsets
from .serializers import BusSerializer, DriverSerializer, RouteSerializer, StudentSerializer, AdminSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import EstProprietaireOuLectureSeulement  # Importez votre permission personnalisée
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout
from .forms import ParentForm 
from .models import SafetyCheck,SecondaryAddressRequest
from .forms import SafetyCheckForm,SecondaryAddressRequestForm
from .models import Schedule, Tarif
from .forms import ScheduleForm, TarifForm


class BusListView(LoginRequiredMixin, ListView):
    model = Bus
    context_object_name = 'buses'
    template_name = 'bus/bus_list.html'

class BusDetailView(LoginRequiredMixin, DetailView):
    model = Bus
    context_object_name = 'bus'
    template_name = 'bus/bus_detail.html'

class BusCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Bus
    fields = ['number', 'capacity', 'model']
    template_name = 'bus/bus_form.html'
    permission_required = 'app.add_bus'

class BusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Bus
    fields = ['number', 'capacity', 'model']
    template_name = 'bus/bus_form.html'
    permission_required = 'app.change_bus'

class BusDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Bus
    context_object_name = 'bus'
    template_name = 'bus/bus_confirm_delete.html'
    success_url = reverse_lazy('bus_list')
    permission_required = 'app.delete_bus'

class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    context_object_name = 'drivers'
    template_name = 'driver/driver_list.html'

class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    context_object_name = 'driver'
    template_name = 'driver/driver_detail.html'

class DriverCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Driver
    fields = ['first_name', 'last_name', 'license_number', 'bus']
    template_name = 'driver/driver_form.html'
    permission_required = 'app.add_driver'

class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Driver
    fields = ['first_name', 'last_name', 'license_number', 'bus']
    template_name = 'driver/driver_form.html'
    permission_required = 'app.change_driver'
    success_url = reverse_lazy('driver_list')  # Assurez-vous d'avoir une URL nommée 'driver_list'

class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Driver
    template_name = 'driver/driver_confirm_delete.html'
    permission_required = 'app.delete_driver'
    success_url = reverse_lazy('driver_list')  # Assurez-vous d'avoir une URL nommée 'driver_list'


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    context_object_name = 'routes'
    template_name = 'route/route_list.html'

class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    context_object_name = 'route'
    template_name = 'route/route_detail.html'

class RouteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Route
    fields = ['name', 'start_point', 'end_point', 'buses']
    template_name = 'route/route_form.html'
    permission_required = 'app.add_route'

class RouteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Route
    fields = ['name', 'start_point', 'end_point', 'buses']
    template_name = 'route/route_form.html'
    permission_required = 'app.change_route'

class RouteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Route
    context_object_name = 'route'
    template_name = 'route/route_confirm_delete.html'
    success_url = reverse_lazy('route_list')
    permission_required = 'app.delete_route'


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student/student_list.html'

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'student/student_detail.html'

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'grade']
    template_name = 'student/student_form.html'
    permission_required = 'app.add_student'

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'grade']
    template_name = 'student/student_form.html'
    permission_required = 'app.change_student'

class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    context_object_name = 'student'
    template_name = 'student/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    permission_required = 'app.delete_student'

class AdminListView(LoginRequiredMixin, ListView):
    model = Admin
    context_object_name = 'admins'
    template_name = 'admin/admin_list.html'

class AdminDetailView(LoginRequiredMixin, DetailView):
    model = Admin
    context_object_name = 'admin'
    template_name = 'admin/admin_detail.html'

class AdminCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Admin
    fields = ['user', 'job_title']
    template_name = 'admin/admin_form.html'
    permission_required = 'app.add_admin'

class AdminUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Admin
    fields = ['user', 'job_title']
    template_name = 'admin/admin_form.html'
    permission_required = 'app.change_admin'

class AdminDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Admin
    context_object_name = 'admin'
    template_name = 'admin/admin_confirm_delete.html'
    success_url = reverse_lazy('admin_list')
    permission_required = 'app.delete_admin'


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer



class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')  # L'email est optionnel

        # Vérifie si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return Response({"error": "Un utilisateur avec ce nom d'utilisateur existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

        # Crée l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)

        # Génère un jeton d'authentification pour l'utilisateur
        token = Token.objects.create(user=user)

        # Retourne la réponse avec le jeton d'authentification
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]    


def user_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def user_dashboard(request):
    return render(request, 'BusManagement_App/user_dashboard.html', {'user': request.user})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def parent_dashboard(request):
    # Ici, vous pouvez ajouter toute logique spécifique nécessaire pour récupérer
    # les informations que vous voulez afficher dans le tableau de bord des parents.
    # Par exemple, récupérer les enfants associés au parent, les messages, les annonces, etc.

    context = {
        # 'enfants': enfants,  # Supposons que vous ayez une liste d'enfants associés
        # 'annonces': annonces,  # Supposons que vous ayez des annonces à afficher
        # Ajoutez ici d'autres contextes si nécessaire
    }

    return render(request, 'BusManagement_App/parent_dashboard.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Directeurs').exists():
                login(request, user)
                return redirect('director_dashboard')
            elif user.groups.filter(name='Parents').exists():
                login(request, user)
                return redirect('parent_dashboard')
            else:
                return HttpResponse("Vous n'avez pas les droits nécessaires.")
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'BusManagement_App/home.html')

@login_required
def director_dashboard(request):
    # Assurez-vous que l'utilisateur est un directeur
    if not request.user.groups.filter(name='Directeurs').exists():
        return HttpResponse("Accès refusé.")

    # Logique pour récupérer les informations nécessaires
    buses = Bus.objects.all()
    # Plus de logique selon les besoins

    return render(request, 'BusManagement_App/director_dashboard.html', {'buses': buses})
 # Assurez-vous d'avoir un formulaire ParentForm

from django.contrib.auth.models import User, Group
from .forms import ParentForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def ajouter_parent(request):
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur et l'ajouter au groupe 'Parents'
            user = form.save()

            # Rediriger vers le tableau de bord des parents
            return redirect('parent_dashboard')
    else:
        form = ParentForm()

    # Afficher le formulaire
    return render(request, 'BusManagement_App/ajouter_parent.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BusForm  # Assurez-vous d'avoir un formulaire BusForm

@login_required
def ajouter_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('director_dashboard')  # Redirigez vers le tableau de bord directeur
    else:
        form = BusForm()
    return render(request, 'BusManagement_App/ajouter_bus.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ChauffeurForm  # Assurez-vous d'avoir un formulaire ChauffeurForm

@login_required
def ajouter_chauffeur(request):
    if request.method == 'POST':
        form = ChauffeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('director_dashboard')  # Redirigez vers le tableau de bord directeur
    else:
        form = ChauffeurForm()
    return render(request, 'BusManagement_App/ajouter_chauffeur.html', {'form': form})



def est_directeur(user):
    return user.groups.filter(name='Directeurs').exists()  # Assurez-vous que le groupe 'Directeurs' existe

@login_required
@user_passes_test(est_directeur)
def vue_directeur(request):
    # Logique de la vue pour les directeurs
    return render(request, 'BusManagement_App/directeur_dashboard.html')

def est_parent(user):
    return user.groups.filter(name='Parents').exists()  # Assurez-vous que le groupe 'Parents' existe

@login_required
@user_passes_test(est_parent)
def vue_parent(request):
    # Logique de la vue pour les parents
    return render(request, 'BusManagement_App/parent_dashboard.html')

def home(request):
    return render(request, 'BusManagement_App/home.html')


# Vues pour Schedule
class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('list_schedules')
    template_name = 'schedules/schedule_form.html'

class ScheduleListView(ListView):
    model = Schedule
    context_object_name = 'schedules'
    template_name = 'schedules/schedule_list.html'

class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('list_schedules')
    template_name = 'schedules/schedule_form.html'

class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('list_schedules')
    template_name = 'schedules/schedule_confirm_delete.html'

# Vues pour Tarif
class TarifCreateView(CreateView):
    model = Tarif
    form_class = TarifForm
    success_url = reverse_lazy('list_tarifs')
    template_name = 'tarifs/tarif_form.html'

class TarifListView(ListView):
    model = Tarif
    context_object_name = 'tarifs'
    template_name = 'tarifs/tarif_list.html'

class TarifUpdateView(UpdateView):
    model = Tarif
    form_class = TarifForm
    success_url = reverse_lazy('list_tarifs')
    template_name = 'tarifs/tarif_form.html'

class TarifDeleteView(DeleteView):
    model = Tarif
    success_url = reverse_lazy('list_tarifs')
    template_name = 'tarifs/tarif_confirm_delete.html'


class SafetyCheckCreateView(CreateView):
    model = SafetyCheck
    form_class = SafetyCheckForm
    template_name = 'safetycheck_form.html'
    success_url = '/safetychecks/'

class SafetyCheckListView(ListView):
    model = SafetyCheck
    context_object_name = 'safety_checks'
    template_name = 'safetycheck_list.html'


class SafetyCheckUpdateView(UpdateView):
    model = SafetyCheck
    form_class = SafetyCheckForm
    template_name = 'safetycheck_update_form.html'
    success_url = reverse_lazy('list_safety_checks')  # Assurez-vous que ce nom d'URL est défini dans votre urls.py


class SafetyCheckDeleteView(DeleteView):
    model = SafetyCheck
    template_name = 'safetycheck_confirm_delete.html'
    success_url = reverse_lazy('list_safety_checks')  # Assurez-vous que ce nom d'URL est défini dans votre urls.py


class SecondaryAddressRequestCreateView(CreateView):
    model = SecondaryAddressRequest
    form_class = SecondaryAddressRequestForm
    template_name = 'secondaryaddressrequest_form.html'
    success_url = '/secondary-address-requests/'

class SecondaryAddressRequestListView(ListView):
    model = SecondaryAddressRequest
    context_object_name = 'secondary_address_requests'
    template_name = 'secondaryaddressrequest_list.html'

class SecondaryAddressRequestUpdateView(UpdateView):
    model = SecondaryAddressRequest
    form_class = SecondaryAddressRequestForm
    template_name = 'secondaryaddressrequest_update_form.html'
    success_url = reverse_lazy('list_secondary_address_requests')

class SecondaryAddressRequestDeleteView(DeleteView):
    model = SecondaryAddressRequest
    template_name = 'secondaryaddressrequest_confirm_delete.html'
    success_url = reverse_lazy('list_secondary_address_requests')  # Assurez-vous que ce nom d'URL est défini dans votre urls.py
