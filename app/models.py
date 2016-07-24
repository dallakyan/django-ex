from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
REMINDERTYPE = (
    ('e', 'Email'),
    ('s', 'SMS'),
)

# Create your models here.
class User(AbstractUser):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

	def was_recently_joined(self):
		return self.date_joined >= timezone.now() - datetime.timedelta(days=2)


class Reminder(models.Model):
	author = models.ForeignKey(User, related_name="reminders")
	reminder_type = models.CharField(max_length=1, choices=REMINDERTYPE)
	body = models.TextField(blank=True, null=True)