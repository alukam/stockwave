import json
from decimal import Decimal
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import F, Sum, DecimalField
from django.db.models.functions import Coalesce
from .forms import AttendantRegistrationForm 

# App-specific imports
from sales.models import Sale 
from products.models import Product 
from debtors.models import Debtor


User = get_user_model()

# 1. Access Check
def is_boss(user):
    return user.is_superuser

# 2. Main Dashboard (General View)
@login_required
def dashboard_view(request):
    today = timezone.now().date()
    sales_today = Sale.objects.filter(timestamp__date=today)
    
    revenue_today = sales_today.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    sales_count = sales_today.count()
    
    total_profit = 0
    if request.user.is_superuser:
        total_profit = Sale.objects.aggregate(
            profit=Coalesce(Sum((F('negotiated_price') - F('product__cost_price')) * F('quantity'), 
                   output_field=DecimalField()), Decimal('0'))
        )['profit']
    
    context = {
        'revenue_today': revenue_today,
        'sales_count': sales_count,
        'total_profit': total_profit,
        'low_stock': Product.objects.filter(quantity__lt=10)[:5],
        'recent_sales': Sale.objects.all().order_by('-timestamp')[:5],
    }
    return render(request, 'users/dashboard.html', context)

# 3. Custom Admin Dashboard (Management View)
@login_required
@user_passes_test(is_boss)
def admin_management(request):
    try:
        # 1. Basic Data
        all_users = User.objects.all().order_by('-date_joined')
        
        # 2. Financials (Wrapped in Coalesce to prevent None errors)
        total_profit = Sale.objects.aggregate(
            total=Coalesce(Sum((F('negotiated_price') - F('product__cost_price')) * F('quantity'), 
                    output_field=DecimalField()), Decimal('0'))
        )['total'] or 0

        stock_value = Product.objects.aggregate(
            total=Coalesce(Sum(F('cost_price') * F('quantity'), 
                    output_field=DecimalField()), Decimal('0'))
        )['total'] or 0

        # 3. Debtors
        unpaid_debtors = Debtor.objects.filter(is_paid=False)
        total_debts = sum(d.balance for d in unpaid_debtors)

        # 4. Chart Data (Simplified to empty arrays if it fails)
        chart_dates, chart_totals = [], []
        today = timezone.now().date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            chart_dates.append(day.strftime('%a'))
            chart_totals.append(0.0) # Start with zeros to ensure the page loads

        context = {
            'all_users': all_users,
            'total_profit': total_profit,
            'stock_value': stock_value,
            'total_debts': total_debts,
            'debtors': unpaid_debtors,
            'user_count': all_users.count(),
            'chart_json': json.dumps({'labels': chart_dates, 'totals': chart_totals}),
            'low_stock': Product.objects.filter(quantity__lt=10),
            'total_expenses': 0, 
        }
        return render(request, 'users/admin_management.html', context)
        
    except Exception as e:
        # This will print the EXACT error in your terminal while giving you a basic response
        print(f"CRITICAL DASHBOARD ERROR: {e}")
        return render(request, 'users/admin_management.html', {'error': str(e)})
# 4. User Status Actions
@login_required
@user_passes_test(is_boss)
def toggle_user_status(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user != request.user:
        target_user.is_active = not target_user.is_active
        target_user.save()
        messages.success(request, f"Status updated for {target_user.username}")
    return redirect('admin_management')

# 5. Auth Views
class IMSLoginView(LoginView):
    template_name = 'users/login.html'

# views.py

# 1. Update your import to include your custom form


def register_view(request):
    if request.method == 'POST':
        # CHANGE THIS LINE to use your custom form
        form = AttendantRegistrationForm(request.POST) 
        
        if form.is_valid():
            # Your custom form's .save() already handles 
            # is_approved = False and role = 'ATTENDANT'
            user = form.save() 
            
            messages.success(request, "Registration successful! Pending Admin approval.")
            return redirect('login')
        else:
            # If the form isn't valid, it will show errors 
            # (like 'Username already taken') instead of a 500 error
            messages.error(request, "Please correct the errors below.")
    else:
        # CHANGE THIS LINE TOO
        form = AttendantRegistrationForm() 
        
    return render(request, 'users/register.html', {'form': form})

@login_required
@user_passes_test(is_boss)
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    # Security: Don't let the Boss delete themselves or other Superusers
    if not target_user.is_superuser:
        username = target_user.username
        target_user.delete()
        messages.warning(request, f"User {username} has been removed.")
    else:
        messages.error(request, "You cannot delete a superuser.")
    return redirect('admin_management')