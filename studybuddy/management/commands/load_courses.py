from csv import DictReader
from django.core.management import BaseCommand
from studybuddy.models import Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("in load courses rn")

        if Course.objects.exists():
            return

        for row in DictReader(open("studybuddy/searchData.csv")):
            if not Course.objects.filter(courseTitle=row["Title"]).exists():
                course = Course(
                    courseAbbv=row["Mnemonic"],
                    courseNumber=row["Number"],
                    courseTitle=row["Title"],
                    courseTopic=row["Topic"],
                )
                course.save()
