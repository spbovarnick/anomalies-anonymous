from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Sighting, Comment


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def sightings_index(request):
#     sightings = Sighting.objects.filter(id__lt=100).order_by('datetime')
#     return render(request, 'sightings/index.html', {
#         'sightings': sightings
#     })

def sightings_index(request):
    page_number = request.GET.get('page', 1)
    per_page = 36  # Change this to the number of cards you want to load per request

    sightings = Sighting.objects.all().order_by('-datetime')
    paginator = Paginator(sightings, per_page)
    sightings = paginator.get_page(page_number)

    return render(request, 'sightings/index.html', {
        'sightings': sightings
    })


def sightings_detail(request, sighting_id):
    sighting = Sighting.objects.get(id=sighting_id)
    return render(request, 'sightings/detail.html', {
        'sighting': sighting
    })

def fetch_sightings(request):
    page_number = request.GET.get('page', 1)
    per_page = 9  # Change this to the number of cards you want to load per request

    all_sightings = Sighting.objects.all().order_by('-datetime')
    paginator = Paginator(all_sightings, per_page)
    sightings = paginator.get_page(page_number)

    data = serializers.serialize('json', sightings) # Convert the data to JSON
    return JsonResponse({'data': data, 'has_next': sightings.has_next()})
