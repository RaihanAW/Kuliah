from django.urls import path
from . import views

urlpatterns = [
    path('items/create/',views.create_item, name='create_item'),
    path('items/',views.list_items, name='list_items'),
    path('summary/',views.dashboard_summary, name='dashboard_summary'),
    path('low_stock/',views.low_stock_items, name='low_stock_items'),
    path('category/<int:category_id>/',views.items_by_category, name='items_by_category'),
    path('categories/summary/',views.category_summary, name='category_summary'),
    path('supplier/<int:supplier_id>/',views.supplier_items, name='supplier_items'),
    path('inventory/full/',views.full_inventory, name='full_inventory'),
]