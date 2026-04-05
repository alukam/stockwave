from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime
from django.utils import timezone
from django.db.models.functions import TruncDate
from .models import Sale
from products.models import Product
from django.db.models import Sum, Q  # Added Q here
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    seven_days_ago = today - datetime.timedelta(days=7)

    daily_sales = Sale.objects.filter(timestamp__date__gte=seven_days_ago) \
        .annotate(date=TruncDate('timestamp')) \
        .values('date') \
        .annotate(total=Sum('total_amount')) \
        .order_by('date')

    chart_dates = [data['date'].strftime("%d %b") for data in daily_sales]
    chart_totals = [float(data['total']) for data in daily_sales]

    revenue_today = Sale.objects.filter(timestamp__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    sales_count = Sale.objects.filter(timestamp__date=today).count()
    recent_sales = Sale.objects.all().order_by('-timestamp')[:5]
    low_stock = Product.objects.filter(quantity__lt=5)

    context = {
        'chart_dates': chart_dates,
        'chart_totals': chart_totals,
        'revenue_today': revenue_today,
        'sales_count': sales_count,
        'recent_sales': recent_sales,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard.html', context)

@login_required
def sales_management(request):
    query = request.GET.get('q')
    # Fetch all sales, newest first
    all_sales = Sale.objects.all().order_by('-timestamp')
    
    if query:
        all_sales = all_sales.filter(
            Q(product__name__icontains=query) |
            Q(attendant__username__icontains=query) |
            Q(id__icontains=query)
        )
    
    # Calculate the sum of the filtered results
    overall_total = all_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'sales': all_sales,
        'overall_total': f"{overall_total:,}", # Added comma formatting for UGX
        'query': query
    }
    return render(request, 'sales/sales_management.html', context)


@login_required
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    products = Product.objects.all()

    if request.method == "POST":
        new_product_id = request.POST.get('product')
        new_qty = int(request.POST.get('quantity'))
        new_price = int(request.POST.get('negotiated_price'))

        # Return old stock
        old_product = sale.product
        old_product.quantity += sale.quantity
        old_product.save()

        new_product = get_object_or_404(Product, id=new_product_id)

        if new_product.quantity < new_qty:
            old_product.quantity -= sale.quantity
            old_product.save()
            messages.error(request, f"Not enough stock! Only {new_product.quantity} left.")
            return redirect('edit_sale', sale_id=sale.id)

        sale.product = new_product
        sale.quantity = new_qty
        sale.negotiated_price = new_price
        sale.total_amount = new_qty * new_price
        sale.save()

        new_product.quantity -= new_qty
        new_product.save()

        messages.success(request, "Sale updated successfully!")
        return redirect('sales_management')

    return render(request, 'sales/edit_sale.html', {'sale': sale, 'products': products})
@login_required
def create_sale(request):
    if request.method == 'POST':
        try:
            # 1. Get data and strip any formatting (like commas or '/-')
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity', 0))
            # Clean the price string in case JS sent "1,000"
            price_raw = request.POST.get('negotiated_price', '0').replace(',', '').replace('/-', '').strip()
            negotiated_price = float(price_raw)

            # 2. Validation
            if not product_id:
                messages.error(request, "No product selected!")
                return redirect('add_sale')

            product = Product.objects.get(id=product_id)

            # 3. Stock Check
            if product.quantity < quantity:
                messages.error(request, f"Not enough stock! Only {product.quantity} left.")
                return redirect('add_sale')

            # 4. Save Sale
            Sale.objects.create(
                product=product,
                quantity=quantity,
                negotiated_price=negotiated_price,
                total_amount=quantity * negotiated_price,
                attendant=request.user
            )

            # 5. Update Stock
            product.quantity -= quantity
            product.save()

            messages.success(request, "Sale completed successfully!")
            return redirect('sales_management')

        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
        except Exception as e:
            # This will show you the EXACT error in your terminal
            print(f"CRITICAL ERROR: {e}") 
            messages.error(request, f"System Error: {e}")
            
    products = Product.objects.filter(quantity__gt=0)
    return render(request, 'sales/add_sale.html', {'products': products})

@login_required
def cancel_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    product = sale.product
    product.quantity += sale.quantity
    product.save()
    sale.delete()
    
    messages.warning(request, "Sale cancelled.")
    return redirect('sales_management') # Fixed redirect