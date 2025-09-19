from django.shortcuts import render


def index(request):
	"""Render the Academics page with the main headings and subheadings."""
	context = {
		'page_title': 'Academics',
	}
	return render(request, 'academics/academics.html', context)
