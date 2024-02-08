from django.db.models import F, Value, Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Recipe, ProductRecipeRelations
from .utils import DefaultValues


def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main-page.html')


def navigation(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == 'GET':
        if request.GET.get('add_product_to_recipe'):

            recipe_id, product_id, weight = [
                int(request.GET[elem]) for elem in filter(lambda x: x != 'add_product_to_recipe', request.GET)
            ]

            return redirect('cook:add_product_to_recipe', recipe_id=recipe_id, product_id=product_id, weight=weight)

        elif request.GET.get('cook_recipe'):
            recipe_id = int(request.GET.get('recipe_id'))
            return redirect('cook:cook_recipe', recipe_id=recipe_id)

        elif request.GET.get('show_recipes_without_product'):
            product_id = int(request.GET.get('product_id'))
            return redirect('cook:show_recipes_without_product', product_id=product_id)

    return HttpResponseRedirect('main_page')


def add_product_to_recipe(request: HttpRequest, recipe_id: int, product_id: int, weight: int) -> HttpResponse:
    if request.method == 'GET':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        product = get_object_or_404(Product, id=product_id)

        ProductRecipeRelations.objects.update_or_create(product=product, recipe=recipe, defaults={'weight': weight})

        return render(request, 'cook/add-product-to-recipe.html',
                      {'recipe': recipe, 'product': product})


def cook_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    if request.method == 'GET':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        recipe.products_in_recipe.update(times_used=F('times_used') + Value(DefaultValues.COOK_PRODUCT))

        return render(request, 'cook/cook_recipe.html', {'recipe': recipe})


def show_recipes_without_product(request: HttpRequest, product_id: int):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)

        product_recipes = Recipe.objects.filter(
            ~Q(products_in_recipe__id=product_id) | Q(
                recipe_product__weight__lt=DefaultValues.LOWER_PRODUCT_WEIGHT_BORDER
            )
        ).distinct()

        return render(request, 'cook/show-recipes-without-product.html',
                      {'product_name': product.name, 'product_recipes': product_recipes})
