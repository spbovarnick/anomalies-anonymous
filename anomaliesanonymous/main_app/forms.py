
# flatpickr: https://github.com/monim67/django-flatpickr
# durationwidget: https://github.com/devangpadhiyar/django-durationwidget

from django_flatpickr.widgets import DateTimePickerInput
from durationwidget.widgets import TimeDurationWidget
from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import Sighting, Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class DeleteCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = []

# make sure to run pip3 install django-flatpickr !!!
class SightingForm(ModelForm):
    class Meta:
        model = Sighting
        fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']
        widgets = {
            'datetime': DateTimePickerInput(),
            'duration': TextInput(attrs={'placeholder': 'DD HH:MM:SS'})
        }