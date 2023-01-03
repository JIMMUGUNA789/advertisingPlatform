from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.CompanyProfile)
admin.site.register(models.Follows)
admin.site.register(models.Likes)
admin.site.register(models.Reviews)
admin.site.register(models.CompanyImages)

