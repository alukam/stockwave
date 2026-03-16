from django.shortcuts import render
from django.db.models import Sum, F, Count  # Added F and Count to do math inside the database
from expenses.models import Expense 
from debtors.models import Debtor 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from sales.models import Sale  # Make sure this matches your actual Sales model name
from products.models import Product # Make sure this matches your Product model name

def dashboard(request):

    today = timezone.now().date()
    # This now uses the CORRECT field names from your error message
    revenue_today = Sale.objects.filter(timestamp__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    sales_count = Sale.objects.filter(timestamp__date=today).count()

    # 3. RECENT TRANSACTIONS (Last 5 sales)
    recent_sales = Sale.objects.select_related('product').order_by('-timestamp')[:5]

    # 4. STOCK ALERTS (Products with quantity less than 10)
    low_stock = Product.objects.filter(quantity__lt=10)



def business_audit_view(request):
    # 1. TOTAL GROSS SALES (From Sales App)
    total_gross = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # 2. MONEY DEMANDED (From Debtors App)
    # Calculation: Sum of (total_amount - amount_paid) for all debtors
    debt_data = Debtor.objects.aggregate(
        total_owed=Sum(F('total_amount') - F('amount_paid'))
    )
    total_debt = debt_data['total_owed'] or 0
    
    # 3. ACTUAL CASH COLLECTED
    paid_sum = total_gross - total_debt
    
    # 4. TOTAL EXPENSES (From Expenses App)
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 5. FINAL REMAINING BALANCE (Actual Cash)
    remaining_sum = paid_sum - total_expenses

    context = {
        'total_gross': total_gross,
        'total_debt': total_debt,
        'total_expenses': total_expenses,
        'paid_sum': paid_sum,
        'remaining_sum': remaining_sum,
    }
    return render(request, 'reports/audit.html', context)

    # 5. GRAPH DATA (Last 7 Days)
    chart_dates = []
    chart_totals = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        # Get total for this specific day
        day_total = Sale.objects.filter(timestamp__date=day).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        chart_dates.append(day.strftime('%a')) # 'Mon', 'Tue', etc.
        chart_totals.append(float(day_total))

    context = {
        'revenue_today': revenue_today,
        'sales_count': sales_count,
        'recent_sales': recent_sales,
        'low_stock': low_stock,
        'chart_dates': chart_dates,
        'chart_totals': chart_totals,
    }
    
    return render(request, 'reports/dashboard.html', context)