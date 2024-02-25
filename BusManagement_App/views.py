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
<<<<<<< Updated upstream
from .forms import ParentForm 
=======
>>>>>>> Stashed changes


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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            return HttpResponse("Votre nom d'utilisateur ou mot de passe est incorrect.")
    return render(request, 'BusManagement_App/login.html')

def user_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def user_dashboard(request):
    return render(request, 'BusManagement_App/user_dashboard.html', {'user': request.user})

<<<<<<< Updated upstream
def login_parent(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Parents').exists():
            login(request, user)
            return redirect('parent_dashboard')
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect, ou vous n'avez pas les droits de Parent.")
    return render(request, 'BusManagement_App/login_parent.html')

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


def login_director(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Directeurs').exists():
            login(request, user)
            return redirect('director_dashboard')
        else:
            return HttpResponse("Nom d'utilisateur ou mot de passe incorrect, ou vous n'avez pas les droits de directeur.")
    return render(request, 'BusManagement_App/login_director.html')


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
=======
>>>>>>> Stashed changes
