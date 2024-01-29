from .models import ProductRecipeRelations


def check_unique_rows(formset) -> None:
    """
    Функция проверяет новые записи в таблице ProductRecipeRelations на уникальность колонок product и recipe,
    если находятся неуникальные строки в таблице, то происходит замена старого значения weight на новое

    :param formset: Django formset
    """

    for ind_form_set, form_set in enumerate(formset):
        if form_set.has_changed() and not form_set.initial:

            for ind_f, f in enumerate(formset):
                form_set_product, form_set_recipe = form_set.cleaned_data['product'], form_set.cleaned_data['recipe']
                f_product, f_recipe = f.cleaned_data['product'], f.cleaned_data['recipe']

                if ind_form_set == ind_f:
                    continue
                elif form_set_product == f_product and form_set_recipe == f_recipe:
                    weight = form_set.cleaned_data['weight']

                    ProductRecipeRelations.objects.filter(product=form_set_product, recipe=form_set_recipe).delete()
                    ProductRecipeRelations.objects.create(product=form_set_product, recipe=form_set_recipe,
                                                          weight=weight)
                    return


class DefaultValues:
    LOWER_PRODUCT_WEIGHT_BORDER = 10
    COOK_PRODUCT = 1
    ZERO = 0