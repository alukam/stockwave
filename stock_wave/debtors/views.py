from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import Debtor, PartialPayment
from products.models import Product


# debtors/views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Debtor



# 1. VIEW ALL DEBTORS
def debtor_list(request):
    debtors = Debtor.objects.all().order_by('-created_at')
    return render(request, 'debtors/debtor_list.html', {'debtors': debtors})

# 2. RECORD A NEW DEBT (REDUCES STOCK)
def add_debtor(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        qty_str = request.POST.get('quantity')
        amount_str = request.POST.get('total_amount')
        
        product = get_object_or_404(Product, id=product_id)

        try:
            qty = int(qty_str)
            total_debt = Decimal(amount_str)

            if product.quantity >= qty:
                # Reduce Stock
                product.quantity -= qty
                product.save()

                # Create Debtor
                Debtor.objects.create(
                    name=request.POST.get('name'),
                    phone=request.POST.get('phone'),
                    product=product,
                    quantity=qty,
                    total_amount=total_debt,
                )
                messages.success(request, "Debt recorded and stock updated!")
                return redirect('debtor_list')
            else:
                messages.error(request, f"Not enough stock! Only {product.quantity} left.")
        except (ValueError, TypeError, Decimal.InvalidOperation):
            messages.error(request, "Please enter valid numbers.")

    products = Product.objects.all()
    return render(request, 'debtors/add_debtor.html', {'products': products})

# 3. VIEW HISTORY & PAY PARTIAL AMOUNTS
def debtor_detail(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    
    if request.method == 'POST':
        amount_input = request.POST.get('amount')
        try:
            amount = Decimal(amount_input)
            if amount > 0:
                # Record partial payment
                PartialPayment.objects.create(
                    debtor=debtor,
                    amount_paid=amount
                )
                # Update main record
                debtor.amount_paid += amount
                debtor.save()
                messages.success(request, f"Payment of {amount:,} UGX received!")
            else:
                messages.error(request, "Amount must be greater than zero.")
        except (ValueError, TypeError, Decimal.InvalidOperation):
            messages.error(request, "Invalid payment amount.")
            
        return redirect('debtor_detail', debtor_id=debtor.id)

    return render(request, 'debtors/debtor_detail.html', {'debtor': debtor})



# 4. EDIT A PARTIAL PAYMENT
def edit_payment(request, payment_id):
    payment = get_object_or_404(PartialPayment, id=payment_id)
    debtor = payment.debtor
    
    if request.method == 'POST':
        old_amount = payment.amount_paid
        new_amount = Decimal(request.POST.get('amount'))
        
        # Update Debtor Total: Subtract old, add new
        debtor.amount_paid = (debtor.amount_paid - old_amount) + new_amount
        debtor.save()
        
        # Update Payment Record
        payment.amount_paid = new_amount
        payment.save()
        
        messages.success(request, "Payment updated successfully!")
        return redirect('debtor_detail', debtor_id=debtor.id)
    
    return render(request, 'debtors/edit_payment.html', {'payment': payment})

# 5. DELETE A PARTIAL PAYMENT
def delete_payment(request, payment_id):
    payment = get_object_or_404(PartialPayment, id=payment_id)
    debtor = payment.debtor
    
    # Subtract this amount from the debtor's total paid
    debtor.amount_paid -= payment.amount_paid
    debtor.save()
    
    payment.delete()
    messages.warning(request, "Payment deleted. Balance updated.")
    return redirect('debtor_detail', debtor_id=debtor.id)


# 6. EDIT THE MAIN DEBT RECORD
def edit_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    products = Product.objects.all()
    
    if request.method == 'POST':
        # If the product or quantity changed, stock management gets complex.
        # For now, let's update name, phone, and total amount.
        debtor.name = request.POST.get('name')
        debtor.phone = request.POST.get('phone')
        debtor.total_amount = Decimal(request.POST.get('total_amount'))
        debtor.save()
        
        messages.success(request, f"Updated record for {debtor.name}")
        return redirect('debtor_list')
        
    return render(request, 'debtors/edit_debtor.html', {'debtor': debtor, 'products': products})

# 7. DELETE THE ENTIRE DEBT (RESTORES STOCK)
def delete_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    
    # Restoring the stock
    product = debtor.product
    product.quantity += debtor.quantity
    product.save()
    
    debtor.delete()
    messages.warning(request, "Debt deleted and items returned to stock.")
    return redirect('debtor_list')

def record_payment(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    # For now, just a placeholder to stop the 500 error
    return redirect('admin_management')

def record_payment(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            amount = int(amount)
            # 1. Create the payment record
            PartialPayment.objects.create(
                debtor=debtor,
                amount=amount
            )
            # 2. Update the debtor's balance logic (assuming your model has this)
            debtor.balance -= amount
            if debtor.balance <= 0:
                debtor.is_paid = True
                debtor.balance = 0
            debtor.save()
            
            messages.success(request, f"Payment of {amount} UGX recorded for {debtor.name}")
            return redirect('admin_management')
            
    return render(request, 'debtors/record_payment.html', {'debtor': debtor})