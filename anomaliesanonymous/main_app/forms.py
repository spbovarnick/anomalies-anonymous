# flatpickr: https://github.com/monim67/django-flatpickr
# durationwidget: https://github.com/devangpadhiyar/django-durationwidget

from django_flatpickr.widgets import DateTimePickerInput
from durationwidget.widgets import TimeDurationWidget
from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import Sighting
from django import forms

# make sure to run pip3 install django-flatpickr !!!
# also make sure to run pip3 install django-durationwidget !!!!
class SightingForm(ModelForm):
    class Meta:
        model = Sighting
        fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']
        # duration = forms.DurationField(widget=TimeDurationWidget(show_days=False), required=True)
        widgets = {
            'datetime': DateTimePickerInput(),
            'duration': TextInput(attrs={'placeholder': 'DD HH:MM:SS'})
        }