
from django.forms import ModelForm
from .models import Recipe, Category, Ingredient
from django import forms

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'ingredients']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Добавляем класс "form-control" ко всем полям
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
