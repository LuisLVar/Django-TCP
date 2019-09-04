from django.contrib import admin

# Register your models here.
from .models import Hero
admin.site.register(Hero)

from .models import Image
admin.site.register(Image)