# store/shop/management/commands/load_goods.py

from django.core.management.base import BaseCommand
from django.core import management

class Command(BaseCommand):
    help = 'Загружает данные о товарах из файла fixtures/data.json'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем загрузку данных...")
        try:
            # Вызываем встроенную команду loaddata
            management.call_command('loaddata', 'data.json')
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))