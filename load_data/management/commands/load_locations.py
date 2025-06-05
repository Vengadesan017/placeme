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
