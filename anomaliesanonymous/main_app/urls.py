from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sightings/', views.sightings_index, name='index'),
    path('sightings/account/', views.account, name='account'),
    path('sightings/<int:sighting_id>/', views.sightings_detail, name='detail'),
    path('sightings/<int:sighting_id>/add_comment/', views.add_comment, name='add_comment'),
    path('sightings/<int:fk>/edit_comment/<int:pk>/', views.CommentEdit.as_view(), name='edit_comment'),
    path('sightings/<int:sighting_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('fetch_sightings/', views.fetch_sightings, name='fetch_sightings'),
    path('sightings/create/', views.sightings_create, name='sightings_create'),
    path('sightings/<int:sighting_id>/update/', views.sightings_update, name='sightings_update'),
    path('sightings/<int:pk>/delete/', views.SightingDelete.as_view(), name='sightings_delete'),
    path('sightings/<int:sighting_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
    path('search/', views.sightings_search, name='search'),
]