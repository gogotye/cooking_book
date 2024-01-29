from django.urls import path
from .views import add_product_to_recipe, cook_recipe, show_recipes_without_product, navigation


app_name = 'cook'


urlpatterns = [
    path('navigation/', navigation, name='navigation'),
    path('add-product-to-recipe/<int:recipe_id>-recipe/<int:product_id>-product/<int:weight>-weight/',
         add_product_to_recipe, name='add_product_to_recipe'),
    path('cook-recipe/<int:recipe_id>-recipe/', cook_recipe, name='cook_recipe'),
    path('show-recipes-without-product/<int:product_id>-product/', show_recipes_without_product,
         name='show_recipes_without_product'),
]