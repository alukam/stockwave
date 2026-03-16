from .models import Sale
from django.utils import timezone
from django.db.models import Sum

def totals_processor(request):
    today = timezone.now().date()
    revenue_today = Sale.objects.filter(timestamp__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return {
        'global_revenue_today': revenue_today,
    }