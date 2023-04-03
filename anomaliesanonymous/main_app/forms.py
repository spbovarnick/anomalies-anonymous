from django_flatpickr.widgets import DateTimePickerInput
from django.forms import ModelForm
from .models import Sighting
from django import forms

class SightingForm(ModelForm):
    class Meta:
        model = Sighting
        fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']
        widgets = {
            'datetime': DateTimePickerInput()
        }