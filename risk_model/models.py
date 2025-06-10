from django.db import models

# Create your models here.
# a new model called Loan, inheriting from models.Model (a database model)
class Loan(models.Model):
    loan_amnt = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=20)
    grade = models.CharField(max_length=2)
    funded_amnt = models.DecimalField(max_digits=10, decimal_places=2)
    default_flag = models.BooleanField()

    recoveries = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collection_recovery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"Loan {self.id} - Grade {self.grade}"