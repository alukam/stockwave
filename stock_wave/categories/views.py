from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category

@login_required
def category_list(request):
    # Fetch categories owned by the user (SaaS ready!)
    # Note: If your model doesn't have an 'owner' field yet, 
    # use Category.objects.all() for now.
    categories = Category.objects.all() 
    
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f"Category '{name}' added!")
            return redirect('category_list')
            
    return render(request, 'categories/category_list.html', {'categories': categories})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.warning(request, "Category deleted.")
    return redirect('category_list')