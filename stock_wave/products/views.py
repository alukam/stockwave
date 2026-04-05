from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from categories.models import Category
from django.contrib.auth.decorators import user_passes_test, login_required

# --- PRODUCT / INVENTORY VIEWS ---


def edit_product(request, pk): # This name MUST match 'views.edit_product' in urls.py
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        # Your logic to update the product
        product.name = request.POST.get('name')
        product.quantity = request.POST.get('quantity')
        # ... other fields ...
        product.save()
        return redirect('inventory')
        
    return render(request, 'products/edit_product.html', {'product': product})




@login_required
def product_list(request):
    # select_related('category') is the merged logic for faster loading
    items = Product.objects.select_related('category').all().order_by('name')
    return render(request, 'products/product_list.html', {'items': items})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin, login_url='dashboard') # Redirects attendants to dashboard
def add_product(request):
    if request.method == "POST":
        # 1. Manual extraction (Preserved from your previous logic)
        name = request.POST.get('name')
        qty = request.POST.get('quantity')
        c_price = request.POST.get('cost_price') # Merged: Updated to match new model
        s_price = request.POST.get('selling_price')
        
        # 2. New Shop Labels (Merged from your requirements)
        category_id = request.POST.get('category')
        loc = request.POST.get('location')
        org = request.POST.get('origin')
        desc = request.POST.get('description')
        
        # 3. Handle the Toggle & Photo (Merged)
        fixed_price = True if request.POST.get('is_fixed_price') == 'on' else False
        prod_photo = request.FILES.get('photo') # request.FILES handles the image

        try:
            # Link the category if selected
            category_obj = Category.objects.get(id=category_id) if category_id else None
            
            # 4. Save to Database using the exact Model labels
            Product.objects.create(
                name=name,
                category=category_obj,
                quantity=qty,
                cost_price=c_price,
                selling_price=s_price,
                location=loc,
                origin=org,
                description=desc,
                photo=prod_photo,
                is_fixed_price=fixed_price
            )
            
            messages.success(request, f"Product {name} added successfully!")
            return redirect('inventory')
            
        except Exception as e:
            messages.error(request, f"Could not add product: {e}")

    # Pass categories so they appear in your dropdown select
    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})