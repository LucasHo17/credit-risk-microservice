from rest_framework import serializers
from .models import Loan

class RiskMetricsSerializer(serializers.Serializer):
    loan_id = serializers.CharField()
    pd      = serializers.FloatField(min_value=0.0, max_value=1.0)
    lgd     = serializers.FloatField(min_value=0.0, max_value=1.0)
    ead     = serializers.DecimalField(max_digits=12, decimal_places=2)