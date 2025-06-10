import csv
from django.core.management.base import BaseCommand
from risk_model.models import Loan

class Command(BaseCommand):
    # what shows up when someone runs python manage.py help
    help = 'Import loan data from a CSV file' 

    # one argument: the path to the csv file
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    # this method runs when you execute the command
    def handle(self, *args, **options):
        # open and read csv
        with open(options['csv_file'], newline='', encoding='utf-8') as f:
            # read each row into a dictionary using CSV header as keys
            reader = csv.DictReader(f)
            # process each row
            for row in reader:
                try:
                    # save a new row in the database
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
