from credit_risk_app.models import Loan
from django.db.models import Count, Sum, F

def calculate_pd(group_by="grade"):
    groups = Loan.objects.values(group_by).annotate(
        total_loans=Count('id'),
        total_defaults=Count('id', filter=F('default_flag'))
    )

    result = []
    for g in groups:
        pd = g['total_defaults'] / g['total_loans'] if g['total_loans'] > 0 else 0
        result.append({
            group_by: g[group_by],
            'PD': round(pd, 4),
            'total_loans': g['total_loans'],
            'total_defaults': g['total_defaults']
        })
    return result


def calculate_expected_loss(group_by="grade"):
    groups = Loan.objects.values(group_by).annotate(
        total_loans=Count('id'),
        total_defaults=Count('id', filter=F('default_flag')),
        total_funded=Sum('funded_amnt'),
        total_recoveries=Sum('recoveries'),
        total_fees=Sum('collection_recovery_fee')
    )

    result = []
    for g in groups:
        total_loans = g['total_loans']
        total_defaults = g['total_defaults']
        total_funded = g['total_funded'] or 0
        total_recoveries = g['total_recoveries'] or 0
        total_fees = g['total_fees'] or 0

        if total_loans == 0 or total_funded == 0:
            continue

        pd = total_defaults / total_loans
        ead = total_funded / total_loans
        lgd = (total_funded - total_recoveries + total_fees) / total_funded
        el = pd * lgd * ead

        result.append({
            group_by: g[group_by],
            'PD': round(pd, 4),
            'LGD': round(lgd, 4),
            'EAD': round(ead, 2),
            'EL': round(el, 2),
        })
    return result
