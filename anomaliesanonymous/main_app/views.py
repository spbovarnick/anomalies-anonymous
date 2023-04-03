from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Sighting, Comment
from .forms import SightingForm


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
    per_page = 100  # Change this to the number of cards you want to load per request

    all_sightings = Sighting.objects.all().order_by('-datetime')
    paginator = Paginator(all_sightings, per_page)
    sightings = paginator.get_page(page_number)

    data = serializers.serialize('json', sightings) # Convert the data to JSON
    return JsonResponse({'data': data, 'has_next': sightings.has_next()})

def sightings_create(request):
    context = {}
    form = SightingForm(request.POST)
    if form.is_valid():
        sighting = form.save()
        return render(request, 'sightings/detail.html', {
        'sighting': sighting
    })
    context['form'] = form
    return render(request, 'sightings/sightings_create.html', context)

def sightings_update(request, sighting_id):
    context = {}
    sighting = get_object_or_404(Sighting, id=sighting_id)
    form = SightingForm(request.POST or None, instance=sighting)
    if form.is_valid():
        sighting = form.save()
        return render(request, 'sightings/detail.html', {
        'sighting': sighting
    })
    context["form"] = form
    return render(request, 'sightings/sightings_create.html', context)

# class SightingCreate(CreateView):
#     model = Sighting
#     fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']

class SightingUpdate(UpdateView):
    model = Sighting
    fields = ['datetime', 'city', 'state', 'shape', 'duration', 'description']

class SightingDelete(DeleteView):
    model = Sighting
    success_url = '/sightings'
