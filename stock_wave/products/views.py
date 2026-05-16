from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from .models import Product
from categories.models import Category


# --- HELPER FUNCTIONS ---

def is_admin(user):
    """Check if the logged-in user is a superuser (Shop Owner)."""
    return user.is_superuser

# --- INVENTORY VIEWS ---



@login_required
def product_list(request):
    """Displays all spare parts with search/filter functionality."""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(origin__icontains=query)
        ).select_related('category').order_by('name')
    else:
        products = Product.objects.select_related('category').all().order_by('name')
        
    # CRITICAL: Context key must be 'items' to match the template loop
    return render(request, 'products/product_list.html', {'items': products})


@login_required
@user_passes_test(is_admin, login_url='dashboard')
def add_product(request):
    if request.method == "POST":
        try:
            # 1. Capture Category
            category_name = request.POST.get('category_name', '').strip()
            category_obj, _ = Category.objects.get_or_create(name=category_name)

            # 2. Capture and Clean Numeric Data (Crucial for UGX/Decimals)
            # We use .get(..., 0) to ensure we don't save 'None' to an Integer field
            qty = request.POST.get('quantity') or 0
            cost = request.POST.get('cost_price') or 0
            sell = request.POST.get('selling_price') or 0

            # 3. Create the Product
            Product.objects.create(
                name=request.POST.get('name'),
                category=category_obj,
                cost_price=cost,
                selling_price=sell,
                quantity=qty,
                location=request.POST.get('location'),
                origin=request.POST.get('origin'),
                description=request.POST.get('description'),
                photo=request.FILES.get('photo'),
                # MATCHING: HTML name="is_fixed_price" to Model has_fixed_price
                has_fixed_price='is_fixed_price' in request.POST
            )
            
            messages.success(request, "Spare part added to Stockwave!")
            return redirect('product_list')
            
        except Exception as e:
            messages.error(request, f"Database Error: {e}")

    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def edit_product(request, pk):
    """Update a product using the same 'Type-to-Create' category logic."""
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    
    if request.method == "POST":
        try:
            category_name = request.POST.get('category_name', '').strip()
            category_obj, created = Category.objects.get_or_create(name=category_name)
            
            product.name = request.POST.get('name')
            product.category = category_obj
            product.quantity = request.POST.get('quantity')
            product.cost_price = request.POST.get('cost_price')
            product.selling_price = request.POST.get('selling_price')
            product.location = request.POST.get('location')
            product.origin = request.POST.get('origin')
            product.description = request.POST.get('description')
            
            if request.FILES.get('photo'):
                product.photo = request.FILES.get('photo')
                
            product.has_fixed_price = 'is_fixed_price' in request.POST
            product.save()
            
            messages.success(request, f"Changes to '{product.name}' saved!")
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"Update failed: {e}")
        
    return render(request, 'products/edit_product.html', {
        'product': product, 
        'categories': categories
    })

@login_required
@user_passes_test(is_admin, login_url='dashboard')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.warning(request, f"'{name}' removed from inventory.")
    return redirect('product_list')