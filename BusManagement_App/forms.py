from django import forms
from .models import Parent, Bus, Driver

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['user', 'phone_number', 'address']

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['number', 'capacity', 'model']

class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'license_number', 'bus']
