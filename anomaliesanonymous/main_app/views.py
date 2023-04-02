from django.shortcuts import render
from .models import Sighting, Comment
from django.views.generic.edit import CreateView


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sightings_index(request):
    sightings = Sighting.objects.filter(id__lt=100).order_by('datetime')
    return render(request, 'sightings/index.html', {
        'sightings': sightings 
    })

def sightings_detail(request, sighting_id):
    sighting = Sighting.objects.get(id=sighting_id)
    return render(request, 'sightings/detail.html', {
        'sighting': sighting
    })

class SightingCreate(CreateView):
    model = Sighting
    fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']