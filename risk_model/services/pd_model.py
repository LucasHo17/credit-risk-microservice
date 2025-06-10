from risk_model.models import Loan
from django.db.models import Count, F

def calculate_pd(group_by = "grade"):
    result = []

    groups = Loan.objects.values(group_by).annotate(
        total_loans = Count('id'),
        total_defaults = Count('id', filter=F('default_flag'))
    )

    for g in groups:
        pd = g["total_defaults"]/g["total_loans"] if g["total_loans"] > 0 else 0
        result.append({
            group_by: g[group_by],
            'PD': round(pd,4),
            'total_loans': g['total_loans'],
            'total_defaults': g['total_defaults']
        })
    return result

    
