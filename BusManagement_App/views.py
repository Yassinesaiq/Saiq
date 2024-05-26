from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Bus, Driver, Route, Student, Admin,Parent
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
from .forms import ScheduleForm, TarifForm,ParentEmailForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ChauffeurForm
from django.http import JsonResponse
from django.conf import settings
from .models import GeocodedAddress, Notification
import json
import logging
from .utils import get_geocoded_addresses_for_map, get_second_addresses_for_map
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")

# views.py

def get_geojson_data(request):
    addresses = GeocodedAddress.objects.all()

    features = []
    for address in addresses:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [address.longitude, address.latitude]
            },
            "properties": {
                "name": address.name
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(geojson)




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


from django.shortcuts import render
from .utils import get_geocoded_addresses_for_map, get_second_addresses_for_map
import logging
from django.http import HttpResponse


logger = logging.getLogger(__name__)
from django.http import HttpResponse


def secondaryAddressCleanup():
    records = SecondaryAddressRequest.objects.all()
    for _record in records:

        if timezone.now() > _record.created_at + datetime.timedelta(days=_record.duration):
            _record.delete()


def my_view(request):

    secondaryAddressCleanup()
    # 1. View the table all records of secondary adresses
    # 2. Remove expired rows

    geojson_data = get_geocoded_addresses_for_map()
    second_addresses = get_second_addresses_for_map()
    number_of_drivers = Bus.objects.count()

    print(number_of_drivers)

    logger.debug(f"geojson_data: {geojson_data}")

    response = HttpResponse()
    response.set_cookie(
        'geocode_session',
        'fo42NIlUsCF72sSrXlAIFCukuuqZ5fN7OQgg52JLPlA',
        samesite='None',  # Set SameSite attribute
        secure=True  # Set Secure attribute
    )
    return render(request, 'BusManagement_App/Map.html', {
        'geojson_data': geojson_data,
        "second_addresses": second_addresses,
        "number_of_drivers": number_of_drivers,
        "distance_trigger_km": 0.5
    })


def my_view_Parent(request):

    secondaryAddressCleanup()
    # 1. View the table all records of secondary adresses
    # 2. Remove expired rows

    parent = Parent.objects.get(user=request.user)
    geojson_data = get_geocoded_addresses_for_map(parent=parent)
    second_addresses = get_second_addresses_for_map(parent=parent)
    number_of_drivers = Bus.objects.count()

    print(number_of_drivers)

    logger.debug(f"geojson_data: {geojson_data}")
    
    response = HttpResponse()
    response.set_cookie(
        'geocode_session',
        'fo42NIlUsCF72sSrXlAIFCukuuqZ5fN7OQgg52JLPlA',
        samesite='None',  # Set SameSite attribute
        secure=True  # Set Secure attribute
    )
    return render(request, 'BusManagement_App/Map_Parent.html', {'geojson_data': geojson_data, "second_addresses": second_addresses,'number_of_drivers':number_of_drivers})

from datetime import date

def my_view_Driver(request):

    secondaryAddressCleanup()
    # 1. View the table all records of secondary adresses
    # 2. Remove expired rows

    geojson_data = get_geocoded_addresses_for_map()
    second_addresses = get_second_addresses_for_map()
    number_of_drivers = Bus.objects.count()

    logger.debug(f"geojson_data: {geojson_data}")
    
    response = HttpResponse()
    response.set_cookie(
        'geocode_session',
        'fo42NIlUsCF72sSrXlAIFCukuuqZ5fN7OQgg52JLPlA',
        samesite='None',  # Set SameSite attribute
        secure=True  # Set Secure attribute
    )
    return render(request, 'BusManagement_App/Map_driver.html', {'geojson_data': geojson_data,
                                                                  "second_addresses": second_addresses,
                                                                  'number_of_drivers':number_of_drivers})

def get_routes_api(request):
    # Votre liste de routes avec les adresses à convertir
    routes = Route.objects.all()

    # La liste qui contiendra les données de vos itinéraires avec les coordonnées
    routes_data = []

    for route in routes:
        # Appel à l'API de géocodage pour le point de départ
        start_geocode = requests.get(
            f"https://atlas.microsoft.com/search/address/json?api-version=1.0&subscription-key={settings.AZURE_MAPS_KEY}&query={route.start_point}"
        ).json()

        # Appel à l'API de géocodage pour le point d'arrivée
        end_geocode = requests.get(
            f"https://atlas.microsoft.com/search/address/json?api-version=1.0&subscription-key={settings.AZURE_MAPS_KEY}&query={route.end_point}"
        ).json()

        # Vérifiez que la réponse de l'API contient des résultats avant d'essayer d'accéder aux coordonnées
        if start_geocode['results'] and end_geocode['results']:
            start_coords = start_geocode['results'][0]['position']
            end_coords = end_geocode['results'][0]['position']

            # Ajoutez les données de l'itinéraire avec les coordonnées à votre liste
            routes_data.append({
                'id': route.id,
                'name': route.name,
                'start_point': start_coords,
                'end_point': end_coords
            })

    return JsonResponse(routes_data, safe=False)  # Envoyez la liste des itinéraires avec les coordonnées


class StudentListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        queryset = Student.objects.all()
        return TemplateResponse(request, 'student/student_list.html', {'students': queryset})


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'student/student_detail.html'

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'grade', 'address', 'distance_to_school', 'has_special_needs', 'temporary_disability']
    template_name = 'BusManagement_App/student_form.html'
    permission_required = 'app.add_student'

    def form_valid(self, form):
        # Instance de l'élève sans sauvegarde en base de données
        self.object = form.save(commit=False)
        # Calcul de l'éligibilité
        self.object.check_eligibility()
        if self.object.is_eligible_for_transport:
            # L'élève est éligible, on peut sauvegarder
            self.object.save()
            return super(StudentCreateView, self).form_valid(form)
        else:
            # L'élève n'est pas éligible, on ne sauvegarde pas et on affiche un message
            messages.error(self.request, "Cet élève n'est pas éligible pour le transport scolaire et n'a pas été enregistré.")
            return redirect('student_add')  # Remplacez 'student_add' par le nom de votre URL pour ajouter un élève

    def get_success_url(self):
        # URL de redirection après une création réussie
        return reverse_lazy('student_list')  # Remplacez 'student_list' par le nom de votre URL de liste d'élèves
    


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


def parent_add(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            parent = form.save()  # Sauvegardez le parent et récupérez l'instance
            group = Group.objects.get(name='Parents')  # Obtenez le groupe de parents
            group.user_set.add(parent.user)  # Ajoutez l'utilisateur parent au groupe
            return redirect('parent_list')
    else:
        form = ParentForm()
    return render(request, 'BusManagement_App/parent_form.html', {'form': form})



def parent_edit(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    if request.method == "POST":
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            return redirect('parent_detail', pk=parent.pk)
    else:
        form = ParentForm(instance=parent)
    return render(request, 'BusManagement_App/parent_form.html', {'form': form})


def parent_detail(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    return render(request, 'BusManagement_App/parent_detail.html', {'parent': parent})

def parent_delete(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    parent.delete()
    return redirect('parent_list')


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
    permission_classes = [IsAuthenticated]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        response = super(StudentViewSet, self).list(request, *args, **kwargs)
        # Si vous recevez une demande HTML, renvoyez les données avec le template.
        if request.accepted_renderer.format == 'html':
            return Response({
                'students': response.data
            }, template_name='BusManagement_App/student_list.html')
        # Sinon, renvoyez la réponse API habituelle.
        return response

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]



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


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    return render(request, 'BusManagement_App/user_dashboard.html', {'user': request.user})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Parent
from .utils import get_geocoded_addresses_for_map, get_second_addresses_for_map
from datetime import date
  # Ensure the function is correctly imported

@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    print(f"Logged in Parent: {parent}")
    children = Student.objects.filter(parent=parent)
    safety_checks = SafetyCheck.objects.filter(student__in=children, check_date=date.today())

    # Get the GeoJSON data filtered for the connected parent
    geojson_data = get_geocoded_addresses_for_map(parent=parent)
    second_addresses = get_second_addresses_for_map(parent=parent)

    context = {
        'geojson_data': geojson_data,
        'second_addresses': second_addresses,  # Add secondary addresses if needed
        'number_of_drivers': Bus.objects.count(),  # Adjust according to your needs
        'children': children,
        'safety_checks': safety_checks
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
            elif user.groups.filter(name='Conducteurs').exists():
                login(request, user)
                return redirect('driver_dashboard')
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
    parents = Parent.objects.all()  # Récupérer tous les parents
    chauffeurs = Driver.objects.all()  # Récupérer tous les chauffeurs

    context = {'buses': buses, 'parents': parents, 'chauffeurs': chauffeurs}

    return render(request, 'BusManagement_App/director_dashboard.html', context)


from datetime import date

@login_required
def driver_dashboard(request):
    if not request.user.groups.filter(name='Conducteurs').exists():
        return HttpResponse("Accès refusé.")
    try:
        # Récupérer le bus associé au conducteur
        bus = Driver.objects.get(user=request.user).bus
        # Récupérer les étudiants ayant effectué des vérifications de sécurité pour ce bus
        students = Student.objects.all()

        if request.method == 'POST':
            for student in students:
                checked_in = request.POST.get(f'checked_in_{student.id}', 'off') == 'on'
                SafetyCheck.objects.create(
                    bus=bus,
                    check_date=date.today(),
                    is_passed=checked_in,
                    student=student
                )
            return redirect('driver_dashboard')

        context = {
            'students': students,
        }

        return render(request, 'BusManagement_App/driver_dashboard.html', context)
    except Bus.DoesNotExist:
        # Gérer le cas où aucun bus n'est associé au conducteur
        # Vous pouvez rediriger l'utilisateur vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Aucun bus associé à ce conducteur.")
    
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
            return redirect('director_dashboard')
    else:
        form = ParentForm()

    # Afficher le formulaire
    return render(request, 'BusManagement_App/ajouter_parent.html', {'form': form})

@login_required
def modifier_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            return redirect('director_dashboard')
    else:
        form = ParentForm(instance=parent)

    return render(request, 'BusManagement_App/modifier_parent.html', {'form': form})

@login_required
def supprimer_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == 'POST':
        parent.delete()
        return redirect('director_dashboard')

    return render(request, 'BusManagement_App/supprimer_parent.html', {'parent': parent})

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
    template_name = 'Check_student.html'


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

@login_required
def profil_parent(request):
    parent = request.user.parent
    return render(request, 'BusManagement_App/profil_parent.html', {'parent': parent})

@login_required
def update_parent_email(request):
    parent = Parent.objects.get(user=request.user)
    if request.method == 'POST':
        form = ParentEmailForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre adresse e-mail a été mise à jour avec succès.")
            return redirect('update_parent_email')
    else:
        form = ParentEmailForm(instance=parent)

    return render(request, 'BusManagement_App/parent_parametre.html', {'form': form})

@login_required
def parent_notification(request):
    parent = request.user.parent
    students = parent.enfants.all()
    notifications = Notification.objects.filter(student_id__in=[student.id for student in students])

    return render(request, 'BusManagement_App/parent_notification.html', {'notifications': notifications})


from django.http import JsonResponse
import requests
def get_azure_maps_token(request):
    # Make a request to the Azure Maps API to get the token
    azure_maps_api_url = 'https://samples.azuremaps.com/api/GetAzureMapsToken'
    response = requests.get(azure_maps_api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and extract the token
        data = response.json()
        token = data.get('token')

        # Return the token as a JSON response
        return JsonResponse({'token': token})
    else:
        # If the request fails, return an error response
        return JsonResponse({'error': 'Failed to retrieve Azure Maps token'}, status=response.status_code)


# BusManagement_App/views.py

from django.http import HttpResponse
from .utils import geocode_and_save_addresses

def geocode_students(request):
    geocode_and_save_addresses()
    return HttpResponse("Les adresses des étudiants ont été géocodées et enregistrées avec succès.")

import datetime
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .forms import SecondaryAddressRequestForm
from .models import Parent, SecondaryAddressRequest, Student

from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from .models import Parent, Student, SecondaryAddressRequest
from .forms import SecondaryAddressRequestForm

def update_address(request):
    parent = Parent.objects.get(user=request.user)
    children = Student.objects.filter(parent=parent)

    if children.exists():
        try:
            secondary_address_request = SecondaryAddressRequest.objects.get(student__in=children)
        except SecondaryAddressRequest.DoesNotExist:
            # If no SecondaryAddressRequest exists, create one for the first child
            first_child = children.first()
            secondary_address_request = SecondaryAddressRequest.objects.create(
                student=first_child,
                address='',
                is_approved=False,
                duration=0,
                longitude=0.0,
                latitude=0.0
            )
    else:
        # Handle the case where the parent has no children
        raise Http404("No children found for this parent.")

    if request.method == 'POST':
        form = SecondaryAddressRequestForm(request.POST, instance=secondary_address_request, parent=parent)
        if form.is_valid():
            # Save the form for the initial secondary address request
            secondary_address_request = form.save()

            # Update the expiration date for the initial secondary address request
            update_expiration_date(secondary_address_request)

            if children.count() > 1:
                # Update the secondary address for all children of the parent
                for child in children:
                    if child != secondary_address_request.student:  # Skip the initial child already updated
                        # Create or update the secondary address request for each child
                        secondary_address_request,created = SecondaryAddressRequest.objects.update_or_create(
                            student=child,
                            defaults={
                                'address': secondary_address_request.address,
                                'is_approved': secondary_address_request.is_approved,
                                'duration': secondary_address_request.duration,
                                'longitude': secondary_address_request.longitude,
                                'latitude': secondary_address_request.latitude
                            }
                        )
                        # Update the expiration date for each secondary address request
                        update_expiration_date(secondary_address_request)

            return redirect('parent_dashboard')  # Redirect to parent dashboard or any other desired URL
    else:
        form = SecondaryAddressRequestForm(instance=secondary_address_request, parent=parent)

    return render(request, 'BusManagement_App/update_address.html', {'form': form})




def update_expiration_date(secondary_address_request):
    # Calculate the expiration date based on the current date and the duration in days
    current_date = timezone.now()
    expiration_date = current_date + timedelta(days=secondary_address_request.duration)

    # Store the expiration date in the model
    secondary_address_request.expiration_date = expiration_date
    secondary_address_request.save()


def process_notification(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        student_id = body_data['student_id']
        message = body_data['message']

        Notification.objects.create(student_id=student_id, message=message)

        return HttpResponse("Notification received and stored successfully.")
    return HttpResponse("Invalid request method.")


