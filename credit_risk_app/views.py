from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from credit_risk_app.serializers import RiskMetricsSerializer
from credit_risk_app.services.capital_calculator import calculate_capital

from django.http import HttpResponse

# Create your views here.
class CapitalCalculationView(APIView):
    def post(self, request):
        serializer = RiskMetricsSerializer(data=request.data)
        if serializer.is_valid():
            result = calculate_capital(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return HttpResponse("Hello from the Homepage!")
