from django.contrib import admin

from .models import Version, Task

admin.site.register(Version)
admin.site.register(Task)
