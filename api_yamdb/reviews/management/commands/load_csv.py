import csv
from django.utils import timezone
from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    """ Загрузчик csv файлов."""
    help = "Loads csv files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                compositions_category = Category.objects.get_or_create(
                    pk=row[0],
                    name=row[1],
                    slug=row[2],
                )
                compositions_genre = Genre.objects.get_or_create(
                    pk=row[0],
                    name=row[1],
                    slug=row[2],
                )
                compositions = Title.objects.get_or_create(pk=row[0],
                                                           name=row[1],
                                                           year=row[2],
                                                           category=compositions_category[0])
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
