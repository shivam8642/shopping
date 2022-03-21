from re import U
from django.contrib import admin
from .models import Product,Slider,Cart,Address,Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Slider)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
