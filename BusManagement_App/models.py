from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    number = models.CharField(max_length=5, unique=True)
    capacity = models.IntegerField()
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"Bus {self.number} - Capacity: {self.capacity}"

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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    grade = models.CharField(max_length=10)
    is_eligible_for_transport = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - Grade: {self.grade} - à Droit au Transport: {self.is_eligible_for_transport} "

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
