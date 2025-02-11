from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeDetailView, HomeView, RecipeCreateView, RecipeEditView, CategoryListView, RecipeDeleteView

app_name = 'recipe'
urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.HomeView.as_view(), name='home'),  # Главная страница
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create/new/', views.RecipeCreateView.as_view(), name='add_recipe'),
    path('recipe/<int:pk>/edit/', views.RecipeEditView.as_view(), name='recipe_edit'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path("recipe/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),


    path('register/', views.register, name='register'),  # Страница регист.
    path('login/', views.login_view, name='login'),  # Страница авториз.
    path('logout/', views.logout_view, name='logout'),  # Страница выхода
    ]

# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),

