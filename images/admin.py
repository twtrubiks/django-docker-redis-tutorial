from django.contrib import admin

# Register your models here.
from images.models import Image

admin.site.register(Image)
