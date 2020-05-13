from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.Master)
admin.site.register(models.Tag)
admin.site.register(models.Suggestion)

admin.site.index_title = 'Admin Panel'
admin.site.site_title = 'Administration'
admin.site.site_header = 'Investment Manager: Administration'
