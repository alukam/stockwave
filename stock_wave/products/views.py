from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from sales.models import Sale 
from products.models import Product
from django.contrib.auth.decorators import user_passes_test, login_required

# --- PRODUCT / INVENTORY VIEWS ---

# Only Managers can see the stock list
@login_required
@user_passes_test(lambda u: u.is_superuser)
def product_list(request):
    items = Product.objects.all().order_by('name')
    return render(request, 'products/product_list.html', {'items': items})

# Only Managers can add new stock
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        qty = request.POST.get('quantity')
        b_price = request.POST.get('buying_price')
        s_price = request.POST.get('selling_price')
        m_price = request.POST.get('min_price')

        Product.objects.create(
            name=name,
            quantity=qty,
            buying_price=b_price,
            selling_price=s_price,
            min_price=m_price
        )
        messages.success(request, f"Product {name} added successfully!")
        return redirect('product_list')
    
    return render(request, 'products/add_product.html')

# --- SALES VIEWS ---

@login_required
def sales_list(request):
    all_sales = Sale.objects.all().order_by('-timestamp')
    overall_total = all_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'sales': all_sales,
        'overall_total': overall_total
    }
    return render(request, 'sales/sales_list.html', context)

@login_required
def create_sale(request):
    if request.method == "POST":
        product_id = request.POST.get('product')
        qty = int(request.POST.get('quantity'))
        user_price = int(request.POST.get('negotiated_price'))
        
        product = get_object_or_404(Product, id=product_id)

        if user_price < product.min_price:
            messages.error(request, f"Price Reject! Minimum allowed is {product.min_price:,} UGX")
            return redirect('add_sale')

        if product.quantity < qty:
            messages.error(request, f"Not enough stock! Only {product.quantity} left.")
            return redirect('add_sale')

        Sale.objects.create(
            product=product,
            attendant=request.user,
            quantity=qty,
            negotiated_price=user_price
        )
        
        product.quantity -= qty
        product.save()
        
        messages.success(request, f"Sale of {product.name} recorded!")
        return redirect('sales_list')

    products = Product.objects.filter(quantity__gt=0) # Only show items actually in stock
    return render(request, 'sales/add_sale.html', {'products': products})

@login_required
@user_passes_test(lambda u: u.is_superuser) # Only boss can cancel a sale!
def cancel_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    product = sale.product
    product.quantity += sale.quantity
    product.save()
    sale.delete()
    
    messages.warning(request, f"Sale cancelled. Items returned to stock.")
    return redirect('sales_list')