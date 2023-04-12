from csv import DictReader
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreToTitle, Review,
                            Title, User,)

MODEL_CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):
    """Загрузчик данных csv. """

    help = 'Import .csv files'

    def handle(self, *args, **options):
        for model, csv in MODEL_CSV.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{csv}',
                    'r', encoding='utf-8'
            ) as csv_file:
                reader = DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Данные из .csv файлов загружены успешно!'))
