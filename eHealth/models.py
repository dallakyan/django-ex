from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

#possibly use this class with one to one correlation with an authorization user class
class Searcher(models.Model):
    GENDER_OPTIONS= (
        ('Other', 'Other'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        )#

    searcher = models.OneToOneField(User)
    #username= models.CharField(max_length=40, unique=True, default=None)
    #password= models.CharField(max_length=32);
    
    
    email= models.EmailField()
    name= models.CharField(max_length=1000)
    surname=models.CharField(max_length=1000)
    age=models.IntegerField(default=0)
    gender=models.CharField(max_length=6, choices=GENDER_OPTIONS)
    # category_list=models.ForeignKey(category_list)
    # search_history=models.ForeignKey(search_history)

    def __unicode__(self):
        return self.username

    #uniquenss= user and name 
class Category(models.Model):
    user=models.ForeignKey(Searcher)
    is_public=models.BooleanField(default=False)
    name=models.CharField(max_length=1000)

    slug = models.SlugField()

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

   #get the category with user and name and from there get the pages 
class Page(models.Model):
    linkURL=models.URLField()
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category)
    visits=models.PositiveIntegerField(default=0)
   # user = models.ForeignKey(Searcher)

    is_public = models.BooleanField(default=False)
    summary=models.CharField(max_length=1000)
    flesch_score=models.PositiveIntegerField()  #pip install textstat
    polarity_score=models.PositiveIntegerField()
    subjectivity_score=models.PositiveIntegerField()

    def __unicode__(self):
        return self.title
    
   
#    # user 
#class Saved_Page(models.Model):
#    link = models.OneToOneField(Page)
#    is_public = models.BooleanField(default=False)
#    user = models.ForeignKey(Searcher)








# class Search(models.Model): #this pertains to the Search History  ("a search" => "searches")
#    query=models.CharField(max_length=1000)
#    timestamp_last_modified=models.DateTimeField(auto_now=True)
#    timestamp_first_time_search_added_to_table=models.DateTimeField(auto_now_add=True)
#     user=models.ForeignKey(Searcher)
#     def __unicode__(self):
#        return self.query
#
#
#
# class Admin(models.Model):
#    contract_email=models.EmailField()
#    hours=models.CharField(max_length=1000)
#    address=models.CharField(max_length=1000)
#     sitename=models.CharField(max_length=100)
#     sitelogo=models.CharField(max_length=100)
#     phone_number=models.CharField(max_length=100)
#     #unicode?

#
# class Favorite_Search(models.Model): #a favorite search has a key to a search
#     query=models.OneToOneField(Search)
#     user=models.ForeignKey(Searcher)
#     #what is the unicdoe? return query.__unicode__()
#

#     saved_timestamp=models.DateTimeField( auto_now_add=True)
#     shared_timestamp=models.DateTimeField(default=timezone.now())#not automatic #really set when public is set true
#     #unicode? link.title?
