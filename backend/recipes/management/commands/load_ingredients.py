import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


def ingr_create(row):
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1],
    )


class Command(BaseCommand):
    help = 'Загрузка из csv файла.'

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(f"{data_path}/data/ingredients.csv", "r",
                  encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ingr_create(row)
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены!'))
