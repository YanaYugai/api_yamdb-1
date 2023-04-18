from csv import DictReader
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User

MODEL_CSV = {
    User: 'static/data/users.csv',
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    Title.genre.through: 'static/data/genre_title.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
}


class Command(BaseCommand):
    """Загрузчик данных csv. """

    help = 'Import .csv files'

    def handle(self, *args, **options):
        for model, csv in MODEL_CSV.items():
            # model.objects.all().delete() Если нужно
            # все очистить, включая удаление superuser
            with open(f'{settings.BASE_DIR}/static/data/{csv}',
                      'r', encoding='utf-8') as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    if 'category' in row:
                        row['category_id'] = row['category']
                        del row['category']
                    if 'author' in row:
                        row['author_id'] = row['author']
                        del row['author']
                    model.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Данные из .csv '
                                             'файлов загружены успешно!'))
