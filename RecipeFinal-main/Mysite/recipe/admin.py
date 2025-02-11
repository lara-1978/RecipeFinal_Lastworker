from django.contrib import admin
from .models import Category, Recipe, Ingredient, RecipeCategory
from django.http import JsonResponse


@admin.action(description="Archive selected recipes")
def mark_archived(modeladmin, request, queryset):
    queryset.update(archived=True)

@admin.action(description="Unarchive selected recipes")
def mark_unarchived(modeladmin, request, queryset):
    queryset.update(archived=False)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'ingredients_short', 'description', 'steps_short', 'cooking_time', 'image', 'author', 'price', 'archived')
    search_fields = ('title',)
    actions = [mark_archived, mark_unarchived, 'export_to_json']

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

    def export_to_json(self, request, queryset):
        recipes = queryset.values('title', 'ingredients')  # ну или что-нибудь другое
        response = JsonResponse(list(recipes), safe=False, json_dumps_params={'ensure_ascii': False})
        response['Content-Disposition'] = 'attachment; filename="recipes.json"'
        return response

    export_to_json.short_description = 'Export selected recipes to JSON'

    def steps_short(self, object: Recipe) -> str:
        if len(object.steps) < 48:
            return object.steps
        return object.steps[:48] + "..."

    # Место для короткого отображения ингредиентов
    def ingredients_short(self, object: Recipe) -> str:
        if len(object.ingredients) < 20:
            return object.ingredients
        return object.ingredients[:20] + "..."


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'category')


# Регистрируем модели
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
