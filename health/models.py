from django.db import models

class Symptom(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SymptomOccurrence(models.Model):
    symptom = models.ForeignKey('Symptom')
    CHOICES = zip(range(1, 11), range(1, 11))
    severity = models.IntegerField(choices=CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(blank=True)

    def __unicode__(self):
        return self.symptom.name

    class Meta:
        ordering = ['-end_time']


class Medicine(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MedicineTaken(models.Model):
    medicine = models.ForeignKey('Medicine')
    dose = models.ForeignKey('food.Quantity')
    time = models.DateTimeField()

    def __unicode__(self):
        return self.medicine.name + ' at ' + str(self.time)

    class Meta:
        ordering = ['-time']


class Weight(models.Model):
    pounds = models.FloatField()
    time = models.DateTimeField()

    def __unicode__(self):
        return self.pounds

    class Meta:
        ordering = ['-time']


class Sleep(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    CHOICES = zip(range(1, 11), range(1, 11))
    how_rested = models.IntegerField(choices=CHOICES)
    times_woke_up = models.IntegerField(default=0)
    with_bed_wedge = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.start_time)

    class Meta:
        ordering = ['-end_time']


class ExerciseActivity(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Exercise(models.Model):
    activity = models.ForeignKey('ExerciseActivity')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return self.activity.name

    class Meta:
        ordering = ['-end_time']


class Event(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class EventOccurrence(models.Model):
    event = models.ForeignKey('Event')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    info = models.TextField(blank=True)

    def __unicode__(self):
        return self.event.name

    class Meta:
        ordering = ['-end_time']
