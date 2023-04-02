from django.shortcuts import render, redirect
from .models import Sighting, Comment
from .forms import CommentForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sightings_index(request):
    sightings = Sighting.objects.filter(id__lt=100).order_by('-datetime')
    return render(request, 'sightings/index.html', {
        'sightings': sightings 
    })

def sightings_detail(request, sighting_id):
    sighting = Sighting.objects.get(id=sighting_id)
    comment_form = CommentForm()
    return render(request, 'sightings/detail.html', {
        'sighting': sighting,
        'comment_form': comment_form,
    })

def add_comment(request, sighting_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.sighting_id = sighting_id
        new_comment.save()
    return redirect('detail', sighting_id=sighting_id)