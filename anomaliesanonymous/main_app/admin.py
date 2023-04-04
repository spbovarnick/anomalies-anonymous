from django.contrib import admin
from .models import Sighting, Comment, Photo

# Register your models here.
admin.site.register(Sighting)
admin.site.register(Comment)
admin.site.register(Photo)