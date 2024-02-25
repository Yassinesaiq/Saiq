from django import forms
from .models import  Bus, Driver
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from .models import SafetyCheck,SecondaryAddressRequest,Schedule, Tarif

class ParentForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('A user with that username already exists.')
        return username

    def save(self):
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        # Récupérer ou créer le groupe 'Parents'
        group, created = Group.objects.get_or_create(name='Parents')
        
        # Ajouter l'utilisateur au groupe 'Parents'
        user.groups.add(group)
        
        # Sauvegarder l'utilisateur
        user.save()

        # Si vous avez d'autres actions à effectuer pour le profil du parent, faites-les ici

        return user

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['number', 'capacity', 'model']

class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'license_number', 'bus']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

class TarifForm(forms.ModelForm):
    class Meta:
        model = Tarif
        fields = '__all__'

class SafetyCheckForm(forms.ModelForm):
    class Meta:
        model = SafetyCheck
        fields = ['bus', 'check_date', 'is_passed']

class SecondaryAddressRequestForm(forms.ModelForm):
    class Meta:
        model = SecondaryAddressRequest
        fields = ['student', 'address', 'is_approved']
