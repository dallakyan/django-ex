from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.forms import widgets
from django import forms

#import autocomplete_light
#autocomplete_light.autodiscover()

from collections import defaultdict
from collections import namedtuple
from datetime import date, timedelta
from matt_django.simple_forms import add_url_to_data
from matt_django.simple_forms import default_model_form
from matt_django.simple_forms import DateTimeWidget
from matt_django.simple_forms import DATE_TIME_FORMATS
from matt_django.simple_forms import simple_form

from food.models import FoodEaten
from food.models import FoodItem
from food.models import FoodItemQuantity
from food.models import FoodItemRating
from food.models import FoodPlanned
from food.models import Measure
from food.models import Quantity
from food.settings import template_base

def base_data():
    data = {}
    data['urls'] = []
    return data


@login_required
def main(request):
    return HttpResponseRedirect(reverse('food-calendar'))


@login_required
def calendar(request):
    data = base_data()
    add_url_to_data(data, 'plan_food', reverse('food-plan-food-ajax'))
    data['days'] = []
    Day = namedtuple('Day', ['day_of_week', 'date', 'meals'])
    Meal = namedtuple('Meal', ['name', 'fooditems', 'add_widget'])
    today = date.today()
    current_date = today
    days_to_show = 7
    for i in range(days_to_show):
        planned_food = FoodPlanned.objects.filter(date=current_date)
        meal_dict = defaultdict(list)
        for food in planned_food:
            meal_dict[food.meal].append(plan_food_widget(current_date,
                                                         food.meal,
                                                         food))
        meals = []
        meals.append(Meal('Breakfast',
                          meal_dict['B'],
                          plan_food_widget(current_date, 'B')))
        meals.append(Meal('Lunch',
                          meal_dict['L'],
                          plan_food_widget(current_date, 'L')))
        meals.append(Meal('Dinner',
                          meal_dict['D'],
                          plan_food_widget(current_date, 'D')))
        data['days'].append(Day(current_date.strftime('%A'), current_date, meals))
        current_date += timedelta(days=1)

    return render(request, template_base + 'calendar.html', data)


@login_required
def eaten(request):
    data = base_data()
    data['food_eaten'] = FoodEaten.objects.all()
    return render(request, template_base + 'eaten.html', data)


@login_required
def recipes(request):
    data = base_data()
    data['food_items'] = FoodItem.objects.all()
    data['form'] = FoodItemAutocompleteForm()
    return render(request, template_base + 'recipes.html', data)

class FoodItemAutocompleteForm(forms.Form):
    food_item = forms.ModelChoiceField(
            FoodItem.objects.all(),)
            #widget=autocomplete_light.ChoiceWidget('FoodItemAutocomplete'))


@login_required
def add_food_eaten(request):
    return simple_form(request, FoodEatenForm, reverse('food-eaten'),
            'Add Food Eaten', 'Add Food Eaten')


@login_required
def edit_food_eaten(request, food_eaten_id):
    fe = get_object_or_404(FoodEaten, pk=food_eaten_id)
    return simple_form(request, FoodEatenForm, reverse('food-eaten'),
            'Edit Food Eaten', 'Edit Food Eaten', instance=fe)


@login_required
def add_food_item(request):
    data = base_data()
    add_url_to_data(data, 'add_ingredient', reverse('food-add-ingredient-ajax'))
    return simple_form(request, FoodItemForm, reverse('food-recipes'),
            'Add Food Item', 'Add Food Item', data=data)


@login_required
def edit_food_item(request, food_item_id):
    f = get_object_or_404(FoodItem, pk=food_item_id)
    data = base_data()
    add_url_to_data(data, 'add_ingredient', reverse('food-add-ingredient-ajax'))
    return simple_form(request, FoodItemForm, reverse('food-recipes'),
            'Edit Food Item', 'Edit Food Item', data=data, instance=f)


@login_required
def add_food_item_rating(request, food_item_id=None):
    data = base_data()
    initial = {}
    if food_item_id:
        initial['food_item'] = food_item_id
    return simple_form(request,
                       default_model_form(FoodItemRating),
                       reverse('food-recipes'),
                       'Rate Food Item',
                       'Rate Food Item',
                       data=data,
                       initial=initial)


@login_required
def edit_food_item_rating(request, food_item_rating_id):
    f = get_object_or_404(FoodItemRating, pk=food_item_rating_id)
    data = base_data()
    return simple_form(request,
                       default_model_form(FoodItemRating),
                       reverse('food-recipes'),
                       'Edit Rating',
                       'Edit Rating',
                       data=data,
                       instance=f)


@login_required
def add_ingredient_ajax(request):
    return HttpResponse(FoodItemQuantityWidget().render('ingredients', None))


@login_required
def create_quantity_ajax(request):
    amount = request.GET['amount']
    m = request.GET['measure']
    try:
        measure = Measure.objects.get(name=m)
    except Measure.DoesNotExist:
        measure = Measure(name=m)
        measure.save()
    try:
        quantity = Quantity.objects.get(amount=amount, measure=measure)
    except Quantity.DoesNotExist:
        quantity = Quantity(amount=amount, measure=measure)
        quantity.save()
    form_field = forms.ModelChoiceField(queryset=Quantity.objects.all())
    return HttpResponse(form_field.widget.render('dose', quantity.id))


@login_required
def plan_food_ajax(request):
    food_item_id = request.GET['planned_food']
    if not food_item_id:
        # By construction, this means that the user changed a select box from
        # containing food to not containing food, which means we should delete
        # the entry.
        plan_id = request.GET['plan_id']
        food_planned = get_object_or_404(FoodPlanned, pk=plan_id)
        food_planned.delete()
        return HttpResponse('')

    food_item = get_object_or_404(FoodItem, pk=food_item_id)
    for_date = request.GET['date']
    meal = request.GET['meal']
    year, month, day = map(int, for_date.split('-'))
    for_date = date(year, month, day)

    plan_id = request.GET['plan_id']
    if plan_id:
        food_planned = get_object_or_404(FoodPlanned, pk=plan_id)
    else:
        food_planned = FoodPlanned(date=for_date, meal=meal)
    food_planned.food_item = food_item
    food_planned.save()
    # Now, the returned result will be a widget, so we need to create that.  If
    # the user _added_ a planned food, we need to return a widget for the food
    # just added, and one for adding a new food.  Otherwise, we just return a
    # new widget for the food we just changed.
    response = plan_food_widget(for_date, food_planned.meal, food_planned)
    if not plan_id:
        response += plan_food_widget(for_date, meal)
    return HttpResponse(response)


def plan_food_widget(date_to_add, meal, planned_food=None):
    if planned_food:
        form_field = forms.ModelChoiceField(queryset=FoodItem.objects.all())
        food_id = planned_food.food_item.id
        plan_id = planned_food.id
        css_class = 'plan-food-select'
    else:
        form_field = forms.ModelChoiceField(
                queryset=FoodItem.objects.all(),
                widget=autocomplete_light.ChoiceWidget('FoodItemAutocomplete'))
        food_id = 0
        plan_id = ''
        css_class = 'plan-food-autocomplete'
    return form_field.widget.render('planned_food', food_id,
                                    {'class': css_class,
                                     'for-date': str(date_to_add),
                                     'meal': meal,
                                     'plan-id': plan_id})


class FoodItemQuantityWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        choices = [('', '----')]
        # We'll fix the choices in this when render is called.
        _widgets = (
                widgets.Select(attrs=attrs, choices=choices),
                widgets.TextInput(attrs=attrs),
                widgets.TextInput(attrs=attrs)
                )
        super(FoodItemQuantityWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [
                    value.food_item.id,
                    value.quantity.amount,
                    value.quantity.measure.name
                    ]
        else:
            return [None, None, None]

    def render(self, name, value, attrs=None):
        # Sorry, variable names are awful.  It's tricky here.  value is what we
        # are passed in - if not None, a list of _ids_ of food items.  values
        # is then the list of food item _objects_ that we pass to
        # self.decompress to get values for each of the widgets to render.
        if not value:
            value = []
        values = []
        for fiq in FoodItemQuantity.objects.filter(id__in=value):
            values.append(fiq)
        if len(values) == 0:
            values = [None]
        items = FoodItem.objects.all()
        choices = [('', '----')]
        for item in items:
            choices.append((item.id, item.name))
        self.widgets[0].choices = choices
        divs = []
        for v in values:
            print 'In loop'
            print v
            div = '<div>'
            sub_v = self.decompress(v)
            for i, widget in enumerate(self.widgets):
                div += widget.render(name + '_%d' % i, sub_v[i], attrs)
            div += '</div>'
            divs.append(div)
        add_div = '<div id="new-ingredient" onclick="add_ingredient()">'
        add_div += 'Add another'
        add_div += '</div>'
        divs.append(add_div)
        return ''.join(divs)

    def value_from_datadict(self, data, files, name):
        # We can't call super here, 'cause we've totally messed with how the
        # results are returned.  This method is fairly complicated.
        print data
        foods = [x for x in data.getlist(name + '_0') if x]
        amounts = [x for x in data.getlist(name + '_1') if x]
        measures = [x for x in data.getlist(name + '_2') if x]
        num_ingredients = len(amounts) # foods might have something in it...
        if num_ingredients == 0 or (num_ingredients == 1 and not amounts[0]):
            return None
        ingredients = []
        for food, amount, measure in zip(foods, amounts, measures):
            f = FoodItem.objects.get(pk=food)
            try:
                m = Measure.objects.get(name=measure)
            except Measure.DoesNotExist:
                m = Measure(name=measure)
                m.save()
            try:
                q = Quantity.objects.get(amount=amount, measure=m)
            except Quantity.DoesNotExist:
                q = Quantity(amount=amount, measure=m)
                q.save()
            try:
                ingredient = FoodItemQuantity.objects.get(food_item=f,
                        quantity=q)
            except FoodItemQuantity.DoesNotExist:
                ingredient = FoodItemQuantity(food_item=f, quantity=q)
                ingredient.save()
            ingredients.append(str(ingredient.id))
        return ingredients


class FoodEatenForm(forms.ModelForm):
    time = forms.DateTimeField(input_formats=DATE_TIME_FORMATS,
                               widget=DateTimeWidget())
    class Meta:
        model = FoodEaten
        fields = '__all__'


class FoodItemForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
            FoodItemQuantity.objects.all(),
            required=False,
            help_text='', # the default help text doesn't apply
            widget=FoodItemQuantityWidget())
    class Meta:
        model = FoodItem
        fields = '__all__'
