from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Bus(models.Model):
    number = models.CharField(max_length=5, unique=True)
    capacity = models.IntegerField()
    model = models.CharField(max_length=50)



class Driver(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    license_number = models.CharField(max_length=20, unique=True)
    bus = models.OneToOneField(Bus, on_delete=models.SET_NULL, null=True, blank=True)  # A driver can have one bus and a bus one driver

    def __str__(self):
        return f"{self.first_name} {self.last_name} - License: {self.license_number}"

class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    buses = models.ManyToManyField(Bus)  # A route can have many buses and a bus can have many routes

    def __str__(self):
        return f"Route {self.name}: {self.start_point} to {self.end_point}"


class Student(models.Model):
    GRADE_CHOICES = [
        ('PS4', 'Préscolaire 4 ans'),
        ('PS5', 'Préscolaire 5 ans'),
        ('CP', 'Cours préparatoire'),
        ('CE1', 'Cours élémentaire 1'),
        ('CE2', 'Cours élémentaire 2'),
        ('CM1', 'Cours moyen 1'),
        ('CM2', 'Cours moyen 2'),
        ('6E', 'Sixième'),
        ('5E', 'Cinquième'),
        ('4E', 'Quatrième'),
        ('3E', 'Troisième'),
        ('2ND', 'Seconde'),
        ('1RE', 'Première'),
        ('TLE', 'Terminale'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='PS4', help_text="Niveau scolaire de l'élève")
    address = models.CharField(max_length=255)
    distance_to_school = models.FloatField(help_text="Distance du domicile à l'école en kilomètres", default='0')
    is_eligible_for_transport = models.BooleanField(default=False)
    has_special_needs = models.BooleanField(default=False)
    temporary_disability = models.BooleanField(default=False)
    
    def check_eligibility(self):
     DISTANCE_CRITERIA_GENERAL = 3  # Tous les élèves à 3km ou plus sont éligibles
     DISTANCE_CRITERIA = {
        'PS4': 0,  # Préscolaire 4 ans toujours éligible
        'PS5': 0.8,  # Préscolaire 5 ans à 0.8 km ou plus
        # Ajouter des critères pour les niveaux primaire et secondaire
        'CP': 1.6, 'CE1': 1.6, 'CE2': 1.6, 'CM1': 1.6, 'CM2': 1.6,  # Primaire
        '6E': 1.6, '5E': 1.6, '4E': 1.6, '3E': 1.6,  # Collège
        '2ND': 1.6, '1RE': 1.6, 'TLE': 1.6,  # Lycée
    }
    
    
     if self.has_special_needs or self.temporary_disability:
        self.is_eligible_for_transport = True
     elif self.distance_to_school >= DISTANCE_CRITERIA_GENERAL:
        self.is_eligible_for_transport = True
     elif self.grade in DISTANCE_CRITERIA and self.distance_to_school >= DISTANCE_CRITERIA[self.grade]:
        self.is_eligible_for_transport = True
     else:
        self.is_eligible_for_transport = False
    
     self.save()
    def __str__(self):
     return f"{self.first_name} {self.last_name} - Grade: {self.grade}  "

class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    CNIE = models.CharField(max_length=30)
    Enfants = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='Parents')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Enfant :{self.Enfants} "    

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin {self.user.first_name} {self.user.last_name} - Job Title: {self.job_title}"
    
class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return f"{self.route.name} - Departure: {self.departure_time}, Arrival: {self.arrival_time}"


class Tarif(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tarifs')
    montant = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"tarif pour {self.route.name}: {self.montant}"
    
class SecondaryAddressRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='secondary_address_requests')
    address = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.student.first_name} for address {self.address}"

class SafetyCheck(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='safety_checks')
    check_date = models.DateField()
    is_passed = models.BooleanField(default=True)

    def __str__(self):
        status = "passed" if self.is_passed else "failed"
        return f"Safety check for {self.bus.number} on {self.check_date}: {status}"
