from django.contrib.auth.models import User
from django.core.management import BaseCommand
from recipe.models import Recipe

class Command(BaseCommand):
    """
    Create recipes
    """
    def handle(self, *args, **options):
        self.stdout.write("create_recipe")
        author = User.objects.first()
        recipe_titles = [
            'ДРАНИКИ КАРТОФЕЛЬНЫЕ С ФАРШЕМ НА СКОВОРОДЕ',
            'КЛЕЦКИ ДЛЯ СУПА ИЗ МУКИ И ЯИЦ',
            'МОЧАНКА ПО БЕЛОРУССКИ С БЛИНАМИ',
            'КАРТОФЕЛЬНАЯ БАБКА В ДУХОВКЕ С ФАРШЕМ',
            'КРАМБАМБУЛЯ БЕЛОРУССКАЯ НАСТОЙКА',
        ]
        for title in recipe_titles:
            recipe, created = Recipe.objects.get_or_create(title=title,  cooking_time=30,  author=author)
            if created:
                self.stdout.write(f"Created recipe: {title}")
            else:
                self.stdout.write(f"Recipe already exists: {title}")

        self.stdout.write(self.style.SUCCESS("Recipes processed"))
