from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sightings/', views.sightings_index, name='index'),
    path('sightings/<int:sighting_id>/', views.sightings_detail, name='detail'),
    path('sightings/create/', views.sightings_create, name='sightings_create'),
    path('sightings/<int:pk>/update', views.sightings_update, name='sightings_update'),
    path('sightings/<int:pk>/delete', views.SightingDelete.as_view(), name='sightings_delete'),
]