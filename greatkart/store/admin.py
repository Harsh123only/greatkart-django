from django.contrib import admin
from .models import Product

# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display=('product_name','slug','description','price','image','stock','is_avilabel')
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Product)