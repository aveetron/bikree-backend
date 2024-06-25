from django.contrib import admin

from shop.models import Shop, Category, Inventory, Sale, SaleDetail

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleDetail)