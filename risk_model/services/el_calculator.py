from risk_model.models import Loan
from django.db.models import Count, Sum, F

def calculate_el(group_by="grade"):
    result = []
    groups = Loan.objects.values(group_by).annotate(
        total_loans = Count('id'),
        total_defaults =  Count('id', filter=F('default_flag')),
        total_funded = Sum('funded_amnt'),
        total_recoveries = Sum('recoveries'),
        total_collection_fees = Sum('collection_recovery_fee')
    )

    for g in groups:
        total_loans = g['total_loans']
        total_defaults = g['total_defaults']
        total_funded = g['total_funded'] or 0
        total_recoveries = g['total_recoveries'] or 0
        total_collection_fees = g['total_collection_fees'] or 0

        if (total_loans == 0 or total_funded == 0):
            continue
        pd = total_defaults/total_loans
        ead = total_funded / total_loans
        loss_amount = total_funded - total_recoveries + total_collection_fees
        lgd = loss_amount / total_funded
        el = pd * ead * lgd

        return result.append({
             group_by: g[group_by],
            'PD': round(pd, 4),
            'LGD': round(lgd, 4),
            'EAD': round(ead, 2),
            'EL': round(el, 2),
        })