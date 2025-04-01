from django.contrib import admin
from .models import CustomUser, Category, MenuItem, Order, CartItem
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(CartItem)
