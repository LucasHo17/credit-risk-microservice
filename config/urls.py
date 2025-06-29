"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from credit_risk_app.views import CapitalCalculationView, PortfolioMetricsView, home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # loan-level risk 
    path('api/loan/<int:loan_id>/risk/', LoanRiskView.as_view(), name='loan-risk'),
    # portfolio-level metrics
    path('api/portfolio/metrics/', PortfolioMetricsView.as_view(), name='portfolio-metrics'),
    # calculate capital
    path('api/calculate-capital/', CapitalCalculationView.as_view(), name='calculate-capital'),
    # loan ingestion
    # path('api/loans/')
]
