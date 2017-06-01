from django.contrib import admin

# Register your models here.

from django.contrib.gis import admin
from .models import Scene, Image, LandsatGrade

admin.site.register(Scene, admin.GeoModelAdmin)

admin.site.register(Image, admin.GeoModelAdmin)
admin.site.register(LandsatGrade, admin.GeoModelAdmin)