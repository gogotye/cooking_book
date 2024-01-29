from django.contrib import admin
from .models import Product, Recipe
from .utils import check_unique_rows


class RecipeInline(admin.StackedInline):
    extra = 1
    model = Recipe.products_in_recipe.through


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    inlines = [RecipeInline]
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        check_unique_rows(formset=formset)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']