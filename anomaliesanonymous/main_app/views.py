# Python modules
import os
import uuid
import boto3
import folium
from folium import plugins

# Django modules
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# App modules
from .models import Sighting, Comment, Photo
from .forms import SightingForm, CommentForm, DeleteCommentForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# SIGHTINGS VIEWS 
# -------------------------------------------------
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
    sighting.user_id = request.user
    comment_form = CommentForm()
    return render(request, 'sightings/detail.html', {
        'sighting': sighting,
        'comment_form': comment_form,
    })

def fetch_sightings(request):
    page_number = request.GET.get('page', 1)
    per_page = 100  # Change this to the number of cards you want to load per request

    all_sightings = Sighting.objects.all().order_by('-datetime')
    paginator = Paginator(all_sightings, per_page)
    sightings = paginator.get_page(page_number)

    data = serializers.serialize('json', sightings) # Convert the data to JSON
    return JsonResponse({'data': data, 'has_next': sightings.has_next()})

@login_required
def account(request):
    sightings = Sighting.objects.filter(user=request.user)
    return render(request, 'sightings/account.html', {
        'sightings': sightings
    })

@login_required
def sightings_create(request):
    context = {}
    form = SightingForm(request.POST)
    if form.is_valid():
        sighting = form.save(commit=False)
        sighting.user = request.user
        sighting.save()
        return redirect('detail', sighting_id=sighting.id)
    context['form'] = form
    return render(request, 'sightings/sightings_create.html', context)

@login_required
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

class SightingDelete(LoginRequiredMixin, DeleteView):
    model = Sighting
    success_url = '/sightings'

# COMMENT VIEWS 
# ------------------------------------------------------- #
@login_required
def add_comment(request, sighting_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.sighting_id = sighting_id
        new_comment.save()
    return redirect('detail', sighting_id=sighting_id)


class CommentEdit(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['comment']


@login_required
def delete_comment(request, sighting_id, comment_id):
    form = DeleteCommentForm(request.POST)
    sighting = get_object_or_404(Sighting, id=sighting_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        return redirect('detail', sighting_id=sighting_id)
    return render(request, 'comment/comment_delete.html', {
        'form': form,
        'sighting': sighting
    })


# PHOTO VIEWS 
# -------------------------------------------------
@login_required
def add_photo(request, sighting_id):
    # photo-file maps to the "name" attr on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # We need a unique "key" (filename) for S3
        # It needs to keep the same file extension as the file that was uploaded (.png, .jpg, .svg, etc)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # Just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # Build the full URL string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # We can assign to sighting_id or sighting (if you have a sighting object)
            Photo.objects.create(url=url, sighting_id=sighting_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', sighting_id=sighting_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # Create a 'user' form object that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Add user to the database
            user = form.save()
            # Log user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again.'
    # There was a bad POST or GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)

# MAP VIEW
# -------------------------------------------------
def map(request):
    base_map = folium.Map(location=[37.0902, -95.7129], tiles='CartoDB Dark_Matter', zoom_start=4)
    base_map = base_map._repr_html_()
    return render(request, 'sightings/map.html', {
        'base_map': base_map
    })
    
    