from django.shortcuts import render
from django.views.generic.base import View

sightings = [
    {'datetime': '10/10/1965 23:45:00', 'city':'norwalk', 'state': 'ct', 'country': 'us', 'shape': 'disk', 'duration': 1200, 'comment': 'A bright orange color changing to reddish color disk/saucer was observed hovering above power transmission lines.', 'latitude': 41.1175, 'longitude': -73.4083333},
    {'datetime': '10/10/1993 22:00:00', 'city':'peoria', 'state': 'il', 'country': 'us', 'shape': 'light', 'duration': 8, 'comment': 'Light over Peoria IL that moves slowly stops in mid-air hovers changes colors shoots in opposite direction and disappears.', 'latitude': 40.6936111, 'longitude': -89.5888889},
    {'datetime': '10/10/1995 17:00:00', 'city':'chester (uk/england)', 'state': None, 'country': 'gb', 'shape': 'circle', 'duration': 20, 'comment': 'Green/Orange circular disc over Chester England.', 'latitude': 40.6936111, 'longitude': -89.5888889},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sightings_index(request):
    return render(request, 'sightings/index.html', {
        'sightings': sightings 
    })