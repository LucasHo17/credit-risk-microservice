import csv
from django.core.management.base import BaseCommand
from risk_model.models import Loan

class Command(BaseCommand):
    help = 'Import loan data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    Loan.objects.create(
                        loan_amnt=row.get('loanAmnt'),
                        term=int(row.get('term', '36').strip().split()[0]),  # '36 months' → 36
                        grade=row.get('grade'),
                        funded_amnt=row.get('fundedAmnt'),
                        default_flag=row.get('reviewStatus') == 'NOT_APPROVED',
                        annual_inc=row.get('annualInc'),
                        interest_rate=row.get('intRate'),
                        home_ownership=row.get('homeOwnership'),
                        purpose=row.get('purpose'),
                        addr_state=row.get('addrState')
                    )
                except Exception as e:
                    self.stderr.write(f"Error on row {row.get('id')}: {e}")

        self.stdout.write(self.style.SUCCESS('CSV import complete.'))
