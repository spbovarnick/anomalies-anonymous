from django.shortcuts import render
from .models import Sighting, Comment

sightings = [
     {
      "datetime": "1996-06-24T07:30:00.000Z",
      "city": "Aurora",
      "state": "CO",
      "shape": "CHA",
      "duration": 3600,
      "description": "Obj. hovered 100 ft above car. Red blue lights on corners. Changed shape from cube to pyramid to triangle. Landed 800 ft away.",
      "latitude": 39.7294444,
      "longitude": -104.8313889
    },
    {
      "datetime": "1998-10-10T09:30:00.000Z",
      "city": "Hollywood",
      "state": "CA",
      "shape": "CHA",
      "duration": 300,
      "description": "I was standing outside on Sunset Blvd. at Vine and looked straight up which I normally do not do. I saw three bright white lights in a",
      "latitude": 34.0983333,
      "longitude": -118.3258333
    },
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sightings_index(request):
    sightings = Sighting.objects.all()
    return render(request, 'sightings/index.html', {
        'sightings': sightings 
    })

def sightings_detail(request, sighting_id):
    sighting = Sighting.objects.get(id=sighting_id)
    return render(request, 'sightings/detail.html', {
        'sighting': sighting
    })