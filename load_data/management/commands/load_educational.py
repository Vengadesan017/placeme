import pandas as pd
from django.core.management.base import BaseCommand
from job_seekers.models import LevelForEdu, CourseForEdu, SpecificationForEdu

class Command(BaseCommand):
    help = 'Load Education data from Master Data_Project.xlsx into the database.'

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
            edhu_df = pd.read_excel(file_path, sheet_name='Education')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        edhu_df = edhu_df.fillna('')

        total_rows = len(edhu_df) 
        count = 0

        for index, row in edhu_df.iterrows():
            level = row['Level'].strip()   # UP # PG
            course = row['Course'].strip()  # B.Tech ..
            speciality = row['Speciality'].strip()

            # Get or create Level
            level_obj, created = LevelForEdu.objects.get_or_create(name=level)

            # Get or create COurce
            course_obj, created = CourseForEdu.objects.get_or_create(name=course, level=level_obj)



            # Create location
            spe_obj, created = SpecificationForEdu.objects.get_or_create(
                name=speciality,
                course=course_obj,
                is_verified=True
            )

            count += 1
            
            self.stdout.write(f"Processing {count}/{total_rows}...")


        self.stdout.write(self.style.SUCCESS(f"✅ Successfully loaded {count} Educational into the database! !!!! Need to set code manually and add type like part/ full time"))
