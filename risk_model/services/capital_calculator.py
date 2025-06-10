from ..serializers import RiskMetricsSerializer
from scipy.stats import norm
import math

def calculate_capital(risk_data: dict):
    """
    risk_data should look like:
      {
        "loan_id": "1234",
        "pd": 0.072,     # 7.2% default prob
        "lgd": 0.45,     # 45% loss given default
        "ead": "10000.00" # decimal or str
      }
    """

    # 1. validate & coerce types
    serializer = RiskMetricsSerializer(data=risk_data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    pd = data['pd']
    lgd = data['lgd']
    ead = float(data['ead'])

    # 2. Compute asset-correlation ρ per Basel II IRB (example formula)
    #    ρ = 0.12·(1−e^(−50·PD))/(1−e^(−50)) + 0.24·(1−(1−e^(−50·PD))/(1−e^(−50)))
    rho = (
        0.12 * (1 - math.exp(-50 * pd)) / (1 - math.exp(-50))
        + 0.24 * (1 - (1 - math.exp(-50 * pd)) / (1 - math.exp(-50)))
    )

    # 3. Capital requirement ratio K:
    #    K = LGD * [Φ( A ) − PD]
    #    where A = sqrt(1/(1−ρ))·Φ⁻¹(PD) + sqrt(ρ/(1−ρ))·Φ⁻¹(0.999)
    inv_pd = norm.ppf(pd)
    inv_999 = norm.ppf(0.999)
    A = (inv_pd * math.sqrt(1/(1 - rho))
         + inv_999 * math.sqrt(rho/(1 - rho)))
    K = lgd * (norm.cdf(A) - pd)

    # 4. Capital amount = K × EAD
    capital_amount = K * ead

    return {
        "loan_id": data['loan_id'],
        "capital_ratio": round(K, 6),       # e.g. 0.035412
        "capital_amount": round(capital_amount, 2)  # in currency units
    }