from csv import DictReader
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Genre, Title,)

MODEL_CSV = {
    #User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title.genre.through: 'genre_title.csv',
    #Review: 'review.csv',
    #Comment: 'comments.csv',
}


class Command(BaseCommand):
    """Загрузчик данных csv. """

    help = 'Import .csv files'

    def handle(self, *args, **options):
        for model, csv in MODEL_CSV.items():
            model.objects.all().delete()
            with open(
                    f'{settings.BASE_DIR}/static/data/{csv}',
                    'r', encoding='utf-8'
            ) as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    if 'category' in row:
                        row['category_id'] = row['category']
                        del row['category']
                    model.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Данные из .csv файлов загружены успешно!'))
