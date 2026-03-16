from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime
from django.utils import timezone
from django.db.models.functions import TruncDate
from .models import Sale
from products.models import Product
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    # 1. Force recalculation of 'today' every time the page is hit
    today = timezone.now().date()
    seven_days_ago = today - datetime.timedelta(days=7)

    # 2. Fetch data directly from the DB inside the view
    daily_sales = Sale.objects.filter(timestamp__date__gte=seven_days_ago) \
        .annotate(date=TruncDate('timestamp')) \
        .values('date') \
        .annotate(total=Sum('total_amount')) \
        .order_by('date')

    # 3. Format data for the chart
    chart_dates = [data['date'].strftime("%d %b") for data in daily_sales]
    chart_totals = [float(data['total']) for data in daily_sales]

    # 4. Get other stats
    revenue_today = Sale.objects.filter(timestamp__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    sales_count = Sale.objects.filter(timestamp__date=today).count()
    recent_sales = Sale.objects.all().order_by('-timestamp')[:5]
    low_stock = Product.objects.filter(quantity__lt=5) # Ensure Product is imported

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
def sales_list(request):
    all_sales = Sale.objects.all().order_by('-timestamp')
    
    # This line does the math in the Database
    # It adds up every 'total_amount' column in the Sale table
    stats = all_sales.aggregate(Sum('total_amount'))
    
    # Extract the number from the dictionary
    overall_total = stats['total_amount__sum'] or 0
    
    context = {
        'sales': all_sales,
        'overall_total': overall_total  # <--- This MUST match the name in HTML
    }
    return render(request, 'sales/sales_list.html', context)


def create_sale(request):
    if request.method == "POST":
        product_id = request.POST.get('product')
        qty = int(request.POST.get('quantity'))
        user_price = int(request.POST.get('negotiated_price'))
        
        product = get_object_or_404(Product, id=product_id)

        # 1. BARGAIN CHECK
        if user_price < product.min_price:
            messages.error(request, f"Price Reject! Minimum allowed is {product.min_price:,} UGX")
            return redirect('add_sale')

        # 2. STOCK CHECK
        if product.quantity < qty:
            messages.error(request, f"Not enough stock! Only {product.quantity} left.")
            return redirect('add_sale')

        # 3. SUCCESS: Calculate total_amount here!
        Sale.objects.create(
            product=product,
            attendant=request.user,
            quantity=qty,
            negotiated_price=user_price,
            total_amount=qty * user_price  # <--- THIS IS THE MISSING PIECE
        )
        
        product.quantity -= qty
        product.save()
        
        messages.success(request, f"Sale of {product.name} recorded!")
        # Redirecting to dashboard lets you see the numbers update immediately
        return redirect('dashboard') 

    products = Product.objects.all()
    return render(request, 'sales/add_sale.html', {'products': products})

def cancel_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    product = sale.product
    
    # Return items to shelf
    product.quantity += sale.quantity
    product.save()
    
    # Delete transaction record
    sale.delete()
    
    messages.warning(request, f"Sale cancelled. {sale.quantity} items returned to {product.name} stock.")
    return redirect('sales_list')

