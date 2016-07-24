import autocomplete_light
from food.models import FoodItem

# This will generate a FoodItemAutocomplete class
#autocomplete_light.register(
        #FoodItem,
        # Just like in ModelAdmin.search_fields
        #search_fields=['name'],
        # This will actually html attribute data-placeholder which will set
        # javascript attribute widget.autocomplete.placeholder.
        # NOTE(matt): I don't understand this yet.
        #autocomplete_js_attributes={'placeholder': 'Other model name ?',},
#)

# vim: et sw=4 sts=4
