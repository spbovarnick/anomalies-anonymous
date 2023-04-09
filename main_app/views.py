# Python modules
import os
import uuid
import boto3
import folium
import geocoder
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
from django.db.models import Q

# App modules
from .models import Sighting, Comment, Photo, User
from .forms import SightingForm, CommentForm, DeleteCommentForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# SIGHTINGS VIEWS
# -------------------------------------------------
def sightings_index(request):
    sorts = ['most-recent', 'oldest', 'newest-posted', 'oldest-posted']
    sort = request.GET.get('sort', sorts[0])
    sightings = None
    if sort == sorts[0]:
        sightings = Sighting.objects.all().order_by('-datetime')
    elif sort == sorts[1]:
        sightings = Sighting.objects.all().order_by('datetime')
    elif sort == sorts[2]:
        sightings = Sighting.objects.all().order_by('-date_posted')
    elif sort == sorts[3]:
        sightings = Sighting.objects.all().order_by('date_posted')

    p = Paginator(sightings, 60)
    page = request.GET.get('page', )
    sightings = p.get_page(page)

    return render(request, 'sightings/index.html', {
        'sightings': sightings,
    })

def sightings_detail(request, sighting_id):
    sighting = Sighting.objects.get(id=sighting_id)
    filer = sighting.user
    sighting.user_id = request.user
    comment_form = CommentForm()
    lat_lng = [sighting.latitude, sighting.longitude]
    detail_map = folium.Map(location=lat_lng, zoom_start=12, tiles='CartoDB Dark_Matter')
    folium.Marker(lat_lng, popup=f"<b>Report #{sighting.id}<b>", icon=folium.Icon(color="cadetblue", icon="bullseye", prefix="fa")).add_to(detail_map)
    detail_map = detail_map._repr_html_()
    return render(request, 'sightings/detail.html', {
        'sighting': sighting,
        'comment_form': comment_form,
        'detail_map': detail_map,
        'filer' : filer,
    })

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
    context = {"form": form, 'sighting': sighting}
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
    user_loc = geocoder.ip('me').latlng
    sightings = Sighting.objects.all()
    sightings_list = Sighting.objects.values_list('latitude', 'longitude')
    base_map = folium.Map(location=user_loc, tiles='CartoDB Dark_Matter', zoom_start=7)
    marker_list = []
    for sighting in sightings:
        marker_list.append([sighting.latitude.__float__(), sighting.longitude.__float__(), sighting.id])
    callback = ('function (row) {' 
                'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                'var icon = L.AwesomeMarkers.icon({'
                "icon: 'bullseye',"
                "iconColor: 'white',"
                "markerColor: 'cadetblue',"
                "prefix: 'fa',"
                    '});'
                'marker.setIcon(icon);'
                "var popup = L.popup({maxWidth: '300'});"
                "popup.setContent(`Report #${row[2]}`);"
                "marker.bindPopup(popup);"
                'return marker};')
    plugins.HeatMap(sightings_list, radius=11).add_to(base_map)
    folium.plugins.FastMarkerCluster(marker_list, callback=callback).add_to(base_map)
    base_map = base_map._repr_html_()
    return render(request, 'sightings/map.html', {
        'base_map': base_map
    })
    
# SEARCH VIEW
# -------------------------------------------------
# This view function takes a search query from the GET parameters and filters the Sighting objects based on the city or state fields.
# If there's no query, it returns an empty queryset.
def sightings_search(request):
    query = request.GET.get('q', '')
    # Empty querysets as default
    sightings = None
    if query:
        if len(Sighting.objects.filter(Q(city__icontains=query) | Q(state__icontains=query) | Q(id__icontains=query) | Q(description__icontains=query) | Q(datetime__icontains=query))) > 0:
            sightings = Sighting.objects.filter(Q(city__icontains=query) | Q(state__icontains=query) | Q(id__icontains=query) | Q(description__icontains=query) | Q(datetime__icontains=query)).order_by('-datetime')
        elif len(User.objects.filter(Q(username__icontains=query))) > 0:
            sightings = User.objects.filter(Q(username__icontains=query))
    else:
        sightings = Sighting.objects.none() # Empty queryset as default
    return render(request, 'sightings/search.html', {'sightings': sightings, 'query': query})
