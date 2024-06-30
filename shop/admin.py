from django.contrib import admin

from shop.models import Category, Inventory, Sale, SaleDetail, Shop

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleDetail)
