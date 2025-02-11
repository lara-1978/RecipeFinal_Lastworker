from django.test import TestCase


class RecipeExportViewTestCase(TestCase):
    fixtures = [
        'recipes-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("recipe:recipe-export"),
        )

        # Проверка, что ответ имеет статус 200
        self.assertEqual(response.status_code, 200)

        # Проверяем, что кодировка UTF-8
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')

        # Загружаем рецепты из БД
        recipes = Recipe.objects.order_by("pk").all()

        # Создаем список с ожидаемыми данными для всех рецептов
        expected_data = [
            {
                "pk": recipe.pk,
                "title": recipe.name,
                "price": str(recipe.price),
                "archived": recipe.archived,
            }
            for recipe in recipes
        ]

        # Получаем данные из ответа в формате JSON
        recipes_data = response.json()

        # Сравниваем полученные данные с ожидаемыми
        self.assertEqual(
            recipes_data["recipes"],
            expected_data
        )
