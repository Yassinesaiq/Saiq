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


    def __str__(self):
        return f"{self.first_name} {self.last_name} - Grade: {self.grade}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin {self.user.first_name} {self.user.last_name} - Job Title: {self.job_title}"