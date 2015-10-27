from django.db import models
from django.contrib import auth
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime

@python_2_unicode_compatible
class User(auth.models.User):

	def __str__(self):
		return r"%s %s" % (self.first_name, self.last_name)

@python_2_unicode_compatible
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = u'User profiles'


@python_2_unicode_compatible
class post(models.Model):
	title = models.TextField()
	body = models.TextField()
	created_time = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('User')

	class Meta:
		ordering = ['-created_time']

	def __str__(self):
		return self.title


@python_2_unicode_compatible
class comment(models.Model):
	author = models.CharField(max_length=60)
	body = models.TextField()
	post = models.ForeignKey(post, related_name="comments", blank=True, null=True)
	created_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return r"%s: %s" % (self.post, self.body[:60])
