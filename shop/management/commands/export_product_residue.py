# store/shop/management/commands/export_product_residue.py

from django.core.management.base import BaseCommand
from django.core import management
from shop.models import Inventory
import json

class Command(BaseCommand):
    help = 'Экспортирует остатки товаров в файл data.json'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем экспорт остатков...")
        try:
            # Используем dumpdata, но ограничиваем выборку моделью Inventory
            management.call_command('dumpdata', 'shop.inventory', format='json', indent=2, output='shop/fixtures/data.json')
            self.stdout.write(self.style.SUCCESS('Остатки успешно экспортированы в shop/fixtures/data.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при экспорте: {e}'))