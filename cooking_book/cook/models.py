from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    times_used = models.PositiveIntegerField(default=0, verbose_name='Кол-во раз использовано в рецепте')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    products_in_recipe = models.ManyToManyField('Product', verbose_name='Состав рецепта',
                                                through='ProductRecipeRelations', related_name='recipes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class ProductRecipeRelations(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name='Рецепт',
                               related_name='recipe_product')
    weight = models.PositiveIntegerField(verbose_name='Вес грамм')

    class Meta:
        verbose_name = 'Отношение "Рецепты-Продукты"'
        verbose_name_plural = 'Отношение "Рецепты-Продукты"'

