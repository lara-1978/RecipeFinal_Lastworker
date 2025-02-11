import json
from django.core.management.base import BaseCommand
from recipe.models import Recipe

class Command(BaseCommand):
    help = 'Экспортирует рецепты в JSON файл'

    def handle(self, *args, **kwargs):
        recipes = Recipe.objects.all().values('title', 'ingredients')  # Или другие поля
        with open('recipes.json', 'w', encoding='utf-8') as f:
            json.dump(list(recipes), f, ensure_ascii=False, indent=4)
        self.stdout.write(self.style.SUCCESS('Export done!'))

