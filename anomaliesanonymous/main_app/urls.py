from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sightings/', views.sightings_index, name='index'),
    path('sightings/<int:sighting_id>/', views.sightings_detail, name='detail'),
    path('sightings/create/', views.SightingCreate.as_view(), name='sightings_create'),
    path('sightings/<int:pk>/update', views.SightingUpdate.as_view(), name='sightings_update'),
]