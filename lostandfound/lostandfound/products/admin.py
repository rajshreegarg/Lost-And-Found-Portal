from django.contrib import admin
from django.forms import TextInput
from django.db import models



# Register your models here.
from .models import Lost_Product,ProductImage,UserProfile

class Lost_ProductAdmin(admin.ModelAdmin):
    date_hierarchy='timestamp'
    search_fields=['title','description']
    list_display=['title','description','contact','active','updated']
    list_editable = ['contact','active']
    list_filter=['title','active']
    readonly_fields=['timestamp','updated']
    prepopulated_fields={"slug":("title",)}
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'15'})},
    }
    class Meta:
        model = Lost_Product


admin.site.register(Lost_Product,Lost_ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(UserProfile)
