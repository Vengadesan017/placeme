import pandas as pd
from django.core.management.base import BaseCommand
from recruiters.models import Benefits, Qualifications
from job_seekers.models import Candidates, DomainForSkill, Skills  # Assuming this model exists for foreign key relationships

class Command(BaseCommand):
    help = 'Load benefits, skills, and qualifications data from Excel into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the Excel file',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file']

        try:
            # Load the Excel file into pandas
            excel_df = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        # Process each sheet
        for sheet_name, df in excel_df.items():
            df = df.fillna('')  # Fill NaN values with empty string

            total_rows = len(df)
            count = 0

            if sheet_name == 'Benefits':
                self.stdout.write(self.style.SUCCESS(f"✅ benefits"))
                for index, row in df.iterrows():
                    benefit_name = row['Benefit'].strip()
                    # If 'Created_by' is in the Excel sheet, replace it with your own logic
                    created_by = Candidates.objects.first()  # Example: fetching the first candidate for demo
                    is_verified = True  # Optional column
                    
                    # Create or get Benefits
                    benefit_obj, created = Benefits.objects.get_or_create(
                        benefit=benefit_name,
                        defaults={'Created_by': created_by, 'is_verified': is_verified}
                    )
                    
                    count += 1
                    self.stdout.write(f"Processing {count}/{total_rows} in Benefits sheet...")
                self.stdout.write(self.style.SUCCESS(f"✅ benefits"))

            # if sheet_name == 'DomainsForSkills':
            #     for index, row in df.iterrows():
            #         domain_name = row['Domain'].strip()

            #         # Create or get DomainForSkill
            #         domain_obj, created = DomainForSkill.objects.get_or_create(
            #             name=domain_name
            #         )

            #         count += 1
            #         self.stdout.write(f"Processing {count}/{total_rows} in DomainsForSkills sheet...")

            if sheet_name == 'List of Skills':
                self.stdout.write(self.style.SUCCESS(f"✅ skills"))
                for index, row in df.iterrows():
                    skill_name = row['Professional Area'].strip()   # skill
                    # description = row['Description'].strip() if 'Description' in row else ''
                    domain_name = row['Industry / Business area'].strip()  # domain
                    # created_by = Candidates.objects.first()  # Example: fetching the first candidate for demo
                    is_verified = True
                    
                    domain_obj, created = DomainForSkill.objects.get_or_create(
                    name=domain_name
                    )
                    


                    # Create or get Skills
                    skill_obj, created = Skills.objects.get_or_create(
                        skill=skill_name,
                        domain=domain_obj,
                        defaults={'is_verified': is_verified}
                    )

                    count += 1
                    self.stdout.write(f"Processing {count}/{total_rows} in Skills sheet...")

            if sheet_name == 'Qualifications':
                self.stdout.write(self.style.SUCCESS(f"✅ Qulification"))
                for index, row in df.iterrows():
                    qualification_name = row['Qualification'].strip()
                    created_by = Candidates.objects.first()  # Example: fetching the first candidate for demo
                    is_verified = row['Is Verified'] if 'Is Verified' in row else False

                    # Create or get Qualifications
                    qualification_obj, created = Qualifications.objects.get_or_create(
                        qualification=qualification_name,
                        defaults={'created_by': created_by, 'is_verified': is_verified}
                    )

                    count += 1
                    self.stdout.write(f"Processing {count}/{total_rows} in Qualifications sheet...")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully loaded data into the database!"))






















import pandas as pd
from django.core.management.base import BaseCommand
from recruiters.models import CountryForLoc, StateForLoc, DistrictForLoc, Locations

class Command(BaseCommand):
    help = 'Load locations data from Master Data_Project.xlsx into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the Excel file',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file']

        try:
            locations_df = pd.read_excel(file_path, sheet_name='List of Locations')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        locations_df = locations_df.fillna('')

        total_rows = len(locations_df) 
        count = 0

        for index, row in locations_df.iterrows():
            country_name = row['Country'].strip()
            state_name = row['StateName'].strip()
            district_name = row['District'].strip()
            location_name = row['Office Name'].strip()
            pincode = row['Pincode']

            # Get or create country
            country_obj, created = CountryForLoc.objects.get_or_create(name=country_name)

            # Get or create state
            state_obj, created = StateForLoc.objects.get_or_create(name=state_name, country=country_obj)

            # Get or create district
            district_obj, created = DistrictForLoc.objects.get_or_create(name=district_name, state=state_obj)

            # Create location
            location_obj, created = Locations.objects.get_or_create(
                location=location_name,
                district=district_obj,
                defaults={'pincode': pincode}
            )

            count += 1
            
            self.stdout.write(f"Processing {count}/{total_rows}...")


        self.stdout.write(self.style.SUCCESS(f"✅ Successfully loaded {count} locations into the database!"))
