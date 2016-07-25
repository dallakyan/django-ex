from django.db import models
from django.contrib.auth.models import User

class Visit(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField('Date of visit')
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return self.date.strftime("%m-%d-%Y")

    def get_images(self):
        files = self.file_set.all()
        return [f.image for f in files if f.image]


class Provider(models.Model):
    user = models.ForeignKey(User)
    visits = models.ManyToManyField(Visit)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __unicode__(self):
        return self.last_name + ", " + self.first_name[0]


class File(models.Model):
    user = models.ForeignKey(User)
    visit = models.ForeignKey(Visit)
    image = models.ImageField("Visit image", upload_to="images/", blank=True, null=True)
