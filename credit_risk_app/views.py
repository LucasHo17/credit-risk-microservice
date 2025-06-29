from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Loan

from credit_risk_app.serializers import RiskMetricsSerializer
from credit_risk_app.services.capital_calculator import calculate_capital

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from the Homepage!")

class PortfolioMetricsView(APIView):
    def get(self, request):
        # TODO: capital at risk/economic capital, exposure at default, portfolio size, delinquency rates
        loans = Loan.objects.all()
        total_ead = sum([float(loan.loan_amnt) for loan in loans])
        average_pd = sum([loan.pd or 0.05 for loan in loans]) / len(loans)
        lgd = 0.45 # or avg

        total_expected_loss = sum([float(loan.loan_amnt) * (loan.pd or 0.05) * lgd for loan in loans])
        capital_requirement = sum([calculate_capital(loan.pd or 0.05, lgd, float(loan.loan_amnt)) for loan in loans])

        return Response({
            'average_pd': average_pd,
            'total_ead': total_ead,
            'total_expected_loss': total_expected_loss,
            'capital_ratio': capital_requirement / total_ead,
            'capital_requirement': capital_requirement,
        })

# Create your views here.
class CapitalCalculationView(APIView):
    def post(self, request):
        serializer = RiskMetricsSerializer(data=request.data)
        if serializer.is_valid():
            result = calculate_capital(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


