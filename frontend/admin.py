from django.contrib import admin
from django import forms
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'uploaded_at')
	list_display_links = ('id', 'title')
	search_fields = ('title', 'caption')


from .models import AboutPage, AboutFieldHistory


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'updated_at')
	readonly_fields = ('updated_at',)

	class AboutPageForm(forms.ModelForm):
		class Meta:
			model = AboutPage
			fields = ('mission', 'approach', 'team')
			widgets = {
				'mission': forms.Textarea(attrs={'rows': 5}),
				'approach': forms.Textarea(attrs={'rows': 6}),
				'team': forms.Textarea(attrs={'rows': 5}),
			}

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			# default placeholder texts
			defaults = {
				'mission': 'To cultivate curious, confident, and compassionate learners by providing a safe, stimulating, and inclusive learning environment.',
				'approach': 'Play-based early childhood learning combined with research-backed instructional practices for primary grades. We emphasize hands-on experiences, inquiry, and partnership with families.',
				'team': 'Our teachers are trained professionals with a passion for early years education and ongoing professional development.',
			}

			instance = kwargs.get('instance') if 'instance' in kwargs else None
			for field_name in ('mission', 'approach', 'team'):
				field = self.fields.get(field_name)
				if not field:
					continue
				current = ''
				if self.instance and getattr(self.instance, field_name):
					current = getattr(self.instance, field_name)

				# set placeholder to current content or default
				placeholder = current if current else defaults.get(field_name, '')
				field.widget.attrs.setdefault('placeholder', placeholder)

				# When editing an existing AboutPage, show a short preview as help_text so it's visible
				if self.instance and self.instance.pk and current:
					preview = (current[:200] + '...') if len(current) > 200 else current
					field.help_text = f'Current content preview: {preview}'

	form = AboutPageForm

	def has_add_permission(self, request):
		# Restrict to single AboutPage instance
		if AboutPage.objects.exists():
			return False
		return super().has_add_permission(request)


@admin.action(description='Restore selected history into About page')
def restore_to_about(modeladmin, request, queryset):
	"""Restore the selected AboutFieldHistory into the AboutPage field.

	If multiple histories selected, restore only the most recent per field.
	"""
	from django.contrib import messages

	# Ensure there is an AboutPage instance
	about, _ = AboutPage.objects.get_or_create()

	# For each field, pick the most recent selected history and restore
	by_field = {}
	for h in queryset.order_by('-created_at'):
		if h.field_name not in by_field:
			by_field[h.field_name] = h

	for field, hist in by_field.items():
		setattr(about, field, hist.content)
	about.save()
	messages.success(request, "Selected history restored to About page.")


@admin.register(AboutFieldHistory)
class AboutFieldHistoryAdmin(admin.ModelAdmin):
	list_display = ('field_name', 'created_at', 'short_preview')
	list_filter = ('field_name',)
	ordering = ('-created_at',)
	actions = [restore_to_about]

	def short_preview(self, obj):
		return (obj.content[:120] + '...') if len(obj.content) > 120 else obj.content
	short_preview.short_description = 'Preview'
