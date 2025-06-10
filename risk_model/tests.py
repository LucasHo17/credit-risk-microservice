from django.test import TestCase
from risk_model.models import Loan
from risk_model.services.pd_model import calculate_pd
from risk_model.services.el_calculator import calculate_el


class PDModelTest(TestCase):
    def setUp(self):
        # Create sample Loan data
        Loan.objects.create(grade="A", default_flag=True, funded_amnt=1000)
        Loan.objects.create(grade="A", default_flag=False, funded_amnt=2000)
        Loan.objects.create(grade="B", default_flag=True, funded_amnt=1500)

    def test_calculate_pd(self):
        result = calculate_pd(group_by="grade")
        self.assertEqual(len(result), 2)  # Two grades: A and B
        self.assertEqual(result[0]['PD'], 0.5)  # Grade A: 1 default out of 2 loans
        self.assertEqual(result[1]['PD'], 1.0)  # Grade B: 1 default out of 1 loan

class ELCalculatorTest(TestCase):
    def setUp(self):
        # Create sample Loan data
        Loan.objects.create(grade="A", default_flag=True, funded_amnt=1000, recoveries=200, collection_recovery_fee=50)
        Loan.objects.create(grade="A", default_flag=False, funded_amnt=2000, recoveries=0, collection_recovery_fee=0)
        Loan.objects.create(grade="B", default_flag=True, funded_amnt=1500, recoveries=500, collection_recovery_fee=100)

    def test_calculate_el(self):
        result = calculate_el(group_by="grade")
        self.assertEqual(len(result), 2)  # Two grades: A and B
        self.assertAlmostEqual(result[0]['EL'], 0.2, places=2)  # Expected Loss for Grade A
        self.assertAlmostEqual(result[1]['EL'], 0.4, places=2)  # Expected Loss for Grade B