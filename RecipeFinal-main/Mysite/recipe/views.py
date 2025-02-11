from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RecipeForm, IngredientForm
from django.views.generic import ListView
from .models import Recipe, Category, Ingredient
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Recipe
    template_name = 'recipe/home.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        selected_category_id = self.request.GET.get('category')
        if selected_category_id:
            queryset = queryset.filter(categories__id=selected_category_id)
        return queryset

    def get_context_data(self, **kwargs):
        # Получаем категории и добавляем их в контекст
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category_id'] = self.request.GET.get('category')
        context['username'] = self.request.user.username if self.request.user.is_authenticated else None

        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'

    def recipe_detail(request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        form = RecipeForm(request.POST or None, instance=recipe)

        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('recipe:recipe_detail', pk=recipe.pk)

        return render(request, 'recipe/recipe_detail.html', {'recipe': recipe, 'form': form})


# class RecipeCreateView(CreateView):
#     model = Recipe
#     form_class = RecipeForm
#     template_name = 'recipe/add_recipe.html'
#
#     def get_success_url(self):
#         return reverse_lazy('recipe:recipe_detail', kwargs={'pk': self.object.pk})


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/add_recipe.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe:recipe_detail', kwargs={'pk': self.object.pk})


class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_edit.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipe:home')



class CategoryListView(ListView):
    model = Category
    template_name = 'recipes/category_list.html'
    context_object_name = 'categories'



class RecipeDeleteView(DeleteView):
    model = Recipe
    queryset = Recipe.objects.prefetch_related("categories")
    success_url = reverse_lazy("recipe:home")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class RecipeDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        recipes = Recipe.objects.order_by("pk").all()  #собираем данные по рецептам
        #создаем новую перем.со словарями
        recipes_data = [
            {
                "pk": recipe.pk,
                "title": recipe.name,
                "price": recipe.price,
                "archived": recipe.archived,
            }
            for recipe in recipes
        ]
        return JsonResponse({"recipe": recipes_data})

def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = IngredientForm()
    return render(request, 'recipe/add_ingredient.html', {'form': form})


    # Регистрация пользователя

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('recipe:home')
            else:
                # Если аутентификация не прошла (неполный логин)
                return redirect('recipe:register')
    else:
        form = UserCreationForm()

    return render(request, 'recipe/register.html', {'form': form})


    # Авторизация пользователя


def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Входим в систему
            return redirect('recipe:home')  # Перенаправляем на главную страницу
        else:
            # Если аутентификация не прошла
            return render(request, 'recipe/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'recipe/login.html')
    # Выход пользователя


@login_required
def logout_view(request):
    logout(request)
    return redirect('recipe:home')

