from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Question)
admin.site.register(models.PetCategory)
admin.site.register(models.PetCode)
admin.site.register(models.AIHistory)