from django.shortcuts import render
from .models import Image


def index(request):
    return render(request, 'frontend/index.html')


def gallery(request):
    images = Image.objects.all()
    return render(request, 'frontend/gallery.html', {'images': images})


def about(request):
    """Simple about page explaining the school's mission and approach."""
    from .models import AboutPage, AboutFieldHistory

    about = AboutPage.objects.first()
    # placeholders if AboutPage doesn't exist yet
    placeholders = {
        'mission': "To cultivate curious, confident, and compassionate learners by providing a safe, stimulating, and inclusive learning environment.",
        'approach': "Play-based early childhood learning combined with research-backed instructional practices for primary grades. We emphasize hands-on experiences, inquiry, and partnership with families.",
        'team': "Our teachers are trained professionals with a passion for early years education and ongoing professional development.",
    }

    context = {}
    if about:
        context['mission'] = about.mission or placeholders['mission']
        context['approach'] = about.approach or placeholders['approach']
        context['team'] = about.team or placeholders['team']
    else:
        context.update(placeholders)

    # provide last 5 history items per field for admin reuse
    context['histories'] = {
        'mission': list(AboutFieldHistory.objects.filter(field_name='mission')[:5]),
        'approach': list(AboutFieldHistory.objects.filter(field_name='approach')[:5]),
        'team': list(AboutFieldHistory.objects.filter(field_name='team')[:5]),
    }

    return render(request, 'frontend/about.html', context)
