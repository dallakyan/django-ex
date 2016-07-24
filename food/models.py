from django.db import models

from taggit.managers import TaggableManager

class Quantity(models.Model):
    amount = models.FloatField()
    measure = models.ForeignKey('Measure')

    def __unicode__(self):
        return str(self.amount) + ' ' + self.measure.__unicode__()

    class Meta:
        ordering = ['measure', '-amount']


class Measure(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FoodItem(models.Model):
    name = models.CharField(max_length=128)
    notes = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    # Non-basic food options
    ingredients = models.ManyToManyField('FoodItemQuantity', blank=True)
    num_servings = models.IntegerField(blank=True, null=True)
    # Basic food options
    serving_size = models.ForeignKey('Quantity', blank=True, null=True)
    calories_per_serving = models.IntegerField(blank=True, null=True)
    grams_per_serving = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_ingredients_list(self):
        ingredients = self.ingredients.all()
        if ingredients.count() != 0:
            return '- ' + ', '.join(unicode(i) for i in ingredients)
        else:
            return ''

    class Meta:
        ordering = ['name']


class FoodItemRating(models.Model):
    food_item = models.ForeignKey('FoodItem')
    PERSON_CHOICES = (
            (u'M', u'Matt'),
            (u'S', u'Sabrina'),
            (u'B', u'Beth'),
            (u'R', u'Russell'),
            )
    person = models.CharField(max_length=2, choices=PERSON_CHOICES)
    notes = models.TextField(blank=True)
    CHOICES = zip(range(1, 11), range(1, 11))
    rating = models.IntegerField(choices=CHOICES)


class FoodItemQuantity(models.Model):
    food_item = models.ForeignKey('FoodItem')
    quantity = models.ForeignKey('Quantity')

    def __unicode__(self):
        return (self.quantity.__unicode__() + " of " +
                self.food_item.__unicode__())


class FoodEaten(models.Model):
    food_item = models.ForeignKey('FoodItem')
    servings = models.FloatField()
    time = models.DateTimeField()

    class Meta:
        ordering = ['-time']


class FoodPlanned(models.Model):
    food_item = models.ForeignKey('FoodItem')
    MEAL_CHOICES = (
            (u'B', u'Breakfast'),
            (u'L', u'Lunch'),
            (u'D', u'Dinner'),
            )
    meal = models.CharField(max_length=2, choices=MEAL_CHOICES)
    date = models.DateField()

    class Meta:
        ordering = ['date']
