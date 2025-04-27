from django.shortcuts import render, redirect
from .models import Category, Supplier, Item
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count

@login_required
def create_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        category_id = request.POST['category_id']
        supplier_id = request.POST['supplier_id']
        
        category = Category.objects.get(id=category_id)
        supplier = Supplier.objects.get(id=supplier_id)
        
        Item.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            supplier=supplier,
            created_by=request.user
        )
        return redirect('list_items')
    else:
        categories = Category.objects.all()
        suppliers = Supplier.objects.all()
        return render(request, 'store/create_item.html', {'categories': categories, 'suppliers': suppliers})

@login_required
def list_items(request):
    items = Item.objects.all()
    return render(request, 'store/list_items.html', {'items': items})

@login_required
def dashboard_summary(request):
    total_stock = Item.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_value = Item.objects.aggregate(total=Sum(models.F('price') * models.F('quantity')))['total'] or 0
    average_price = Item.objects.aggregate(Avg('price'))['price__avg'] or 0

    return render(request, 'store/summary.html', {
        'total_stock': total_stock,
        'total_value': total_value,
        'average_price': average_price
    })

@login_required
def low_stock_items(request):
    items = Item.objects.filter(quantity__lt=5)
    return render(request, 'store/low_stock.html', {'items': items})

@login_required
def items_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'store/items_by_category.html', {'category': category, 'items': items})

@login_required
def category_summary(request):
    categories = Category.objects.annotate(
        total_items=Count('item'),
        total_value=Sum(models.F('item__price') * models.F('item__quantity')),
        average_price=Avg('item__price')
    )
    return render(request, 'store/category_summary.html', {'categories': categories})

@login_required
def supplier_items(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    items = Item.objects.filter(supplier=supplier)
    total_items = items.count()
    total_value = items.aggregate(Sum(models.F('price') * models.F('quantity')))['price__sum'] or 0
    return render(request, 'store/supplier_items.html', {'supplier': supplier, 'items': items, 'total_items': total_items, 'total_value': total_value})

@login_required
def full_inventory(request):
    total_items = Item.objects.count()
    total_stock = Item.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_value = Item.objects.aggregate(total=Sum(models.F('price') * models.F('quantity')))['total'] or 0
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    return render(request, 'store/full_inventory.html', {
        'total_items': total_items,
        'total_stock': total_stock,
        'total_value': total_value,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
    })