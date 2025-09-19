from django.db import models


class Image(models.Model):
	title = models.CharField(max_length=200, blank=True)
	image = models.ImageField(upload_to='gallery/')
	caption = models.TextField(blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-uploaded_at']

	def __str__(self):
		return self.title or f"Image {self.pk}"


class AboutPage(models.Model):
	"""Singleton-like model to store editable About page sections."""
	mission = models.TextField(blank=True, help_text="Our Mission text")
	approach = models.TextField(blank=True, help_text="Our Approach text")
	team = models.TextField(blank=True, help_text="Our Team text")
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "About Page Content"

	class Meta:
		verbose_name = "About Page"
		verbose_name_plural = "About Page"


class AboutFieldHistory(models.Model):
	"""Stores historical versions for individual about fields.

	field_name should be one of 'mission', 'approach', 'team'.
	"""
	FIELD_CHOICES = [
		('mission', 'Mission'),
		('approach', 'Approach'),
		('team', 'Team'),
	]
	field_name = models.CharField(max_length=20, choices=FIELD_CHOICES)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.get_field_name_display()} @ {self.created_at:%Y-%m-%d %H:%M}"


# Signals to record history when AboutPage changes
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AboutPage)
def create_about_history(sender, instance, created, **kwargs):
	"""On create or update, store snapshots for fields that changed.

	Keep only the latest 5 entries per field.
	"""
	# If created, store initial snapshots for any non-empty fields
	fields = ['mission', 'approach', 'team']
	for field in fields:
		value = getattr(instance, field, '') or ''
		if created:
			if value.strip():
				AboutFieldHistory.objects.create(field_name=field, content=value)
		else:
			# On update: compare to last saved history; if different, save
			last = AboutFieldHistory.objects.filter(field_name=field).order_by('-created_at').first()
			last_content = last.content if last else ''
			if value.strip() and value.strip() != last_content.strip():
				AboutFieldHistory.objects.create(field_name=field, content=value)

		# Trim to last 5 entries
		qs = AboutFieldHistory.objects.filter(field_name=field).order_by('-created_at')
		extras = qs[5:]
		if extras.exists():
			# delete older entries beyond the 5 most recent
			AboutFieldHistory.objects.filter(pk__in=[o.pk for o in extras]).delete()


