from django.conf.urls import url

from food import views

food_item_id = '(?P<food_item_id>[^/]+)'
food_item_rating_id = '(?P<food_item_rating_id>[^/]+)'
food_eaten_id = '(?P<food_eaten_id>[^/]+)'

urlpatterns = [
    # Main views
    url(r'^$',
        views.main, name='food-main'),
    url(r'^calendar$',
        views.calendar, name='food-calendar'),
    url(r'^recipes$',
        views.recipes, name='food-recipes'),
    url(r'^eaten$',
        views.eaten, name='food-eaten'),
    url(r'^add-food-item$',
        views.add_food_item, name='food-add-food-item'),
    url(r'^edit-food-item/'+food_item_id+'$',
        views.edit_food_item, name='food-edit-food-item'),
    url(r'^add-food-item-rating$',
        views.add_food_item_rating, name='food-add-food-item-rating'),
    url(r'^add-food-item-rating/'+food_item_id+'$',
        views.add_food_item_rating, name='food-add-food-item-rating-with-food'),
    url(r'^edit-food-item-rating/'+food_item_rating_id+'$',
        views.edit_food_item_rating, name='food-edit-food-item-rating'),
    url(r'^add-food-eaten$',
        views.add_food_eaten, name='food-add-food-eaten'),
    url(r'^edit-food-eaten/'+food_eaten_id+'$',
        views.edit_food_eaten, name='food-edit-food-eaten'),
    url(r'^create-quantity-ajax$',
        views.create_quantity_ajax, name='food-create-quantity-ajax'),
    url(r'^add-ingredient-ajax$',
        views.add_ingredient_ajax, name='food-add-ingredient-ajax'),
    url(r'^plan-food-ajax$',
        views.plan_food_ajax, name='food-plan-food-ajax'),
]

# vim: et sw=4 sts=4
