from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework. views import APIView
from recipe.models import Recipe
from .serializers import RecipeSerializer


@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello world"})

 ### Можно и этим методом делать###
# class RecipeView(APIView):
#     def get(self, request:Request) -> Response:
#         recipes = Recipe.objects.all()
#         serialized = RecipeSerializer(recipes, many=True)
#         return Response({"recipes": serialized.data})



   ### А можно и этим методом делать###

class RecipeView(ListCreateAPIView):
    queryset = Recipe.objects.all()  # тут будут запросы ко всем рецептам
    serializer_class = RecipeSerializer  # создаем класс который будет создан для сериализ. данных
# # Create your views here.
