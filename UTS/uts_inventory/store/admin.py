from django.contrib import admin
from .models import Admin, Category, Supplier, Item

admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Item)