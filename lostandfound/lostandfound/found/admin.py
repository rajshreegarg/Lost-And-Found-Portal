from django.contrib import admin

# Register your models here.
from .models import Found

class FoundAdmin(admin.ModelAdmin):
    class Meta:
        model=Found

admin.site.register(Found,FoundAdmin)
