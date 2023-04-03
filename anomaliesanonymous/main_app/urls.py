from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sightings/', views.sightings_index, name='index'),
    path('sightings/<int:sighting_id>/', views.sightings_detail, name='detail'),
    path('sightings/<int:sighting_id>/add_comment/', views.add_comment, name='add_comment'),
    path('sightings/<int:fk>/edit_comment/<int:pk>/', views.CommentEdit.as_view(), name='edit_comment'),
    path('sightings/<int:fk>/delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='delete_comment'),
]