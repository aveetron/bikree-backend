from django.contrib import admin

from shop.models import Shop, Category, Inventory

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Inventory)