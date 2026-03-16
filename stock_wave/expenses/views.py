from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from django.db.models import Sum

@login_required
def expense_list(request):
    all_expenses = Expense.objects.all().order_by('-date')
    total_spent = all_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    if request.method == "POST":
        desc = request.POST.get('description')
        amt = request.POST.get('amount')
        # We use request.user to track who recorded the expense
        Expense.objects.create(
            description=desc, 
            amount=amt, 
            user=request.user
        )
        messages.success(request, f"Recorded: {desc} for {amt} UGX")
        return redirect('expense_list')

    return render(request, 'expenses/expense_list.html', {
        'expenses': all_expenses,
        'total_spent': total_spent
    })

@login_required
def cancel_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    # Security: Only managers or the person who wrote it can delete
    if request.user.is_superuser or request.user == expense.user:
        expense.delete()
        messages.warning(request, "Expense record removed.")
    else:
        messages.error(request, "You don't have permission to delete this.")
    return redirect('expense_list')