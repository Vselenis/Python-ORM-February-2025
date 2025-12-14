import os
import django
from django.db.models import Count, F, Q
from main_app.models import Museum, Curator, Exhibition

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()



def get_museums(search_string=None):
    if search_string is None:
        return "No search criteria provided."

    museums = Museum.objects.filter(
        name__icontains=search_string
    ).order_by('-annual_visitors', 'name')

    if not museums.exists():
        return "No museums matching this search."

    result = []
    for museum in museums:
        result.append(f"Museum: {museum.name}, location: {museum.location}, visitors: {museum.annual_visitors}")
    return "\n".join(result)


def get_top_museum():
    museums = Museum.objects.annotate(
        exhibitions_count=Count('exhibition')
    ).order_by('-exhibitions_count', 'name')

    if not museums.exists():
        return "No museums."

    top_museum = museums.first()
    return f"Top museum: {top_museum.name} /{top_museum.location}/, exhibitions: {top_museum.exhibitions_count}"



def get_curators_by_exhibitions_count():
    curators = Curator.objects.annotate(
        exhibitions_count=Count('exhibition')
    ).order_by('-exhibitions_count', 'name')[:2]

    if not curators.exists():
        return "No curators."

    return "\n".join(
        f"{curator.name}: {curator.exhibitions_count} exhibition/s."
        for curator in curators
    )

def get_top_curator():
    curators = Curator.objects.annotate(
        exhibitions_count=Count('exhibition')
    ).filter(exhibitions_count__gt=0).order_by('-exhibitions_count', 'name')

    if not curators.exists():
        return "No curators meet the criteria."

    top_curator = curators.first()
    exhibitions = top_curator.exhibition_set.all().order_by('name')
    exhibition_names = ", ".join([e.name for e in exhibitions])

    return f"Top curator: {top_curator.name}; Exhibitions: {exhibition_names}."


def get_latest_free_exhibition():
    exhibitions = Exhibition.objects.filter(
        is_free_entry=True
    ).order_by('-opening_date', 'name')

    if not exhibitions.exists():
        return "No exhibitions with free entry."

    top_exhibition = exhibitions.first()
    curators = top_exhibition.curators.all().order_by('name')

    if curators.exists():
        c_names = ", ".join([c.name for c in curators])
    else:
        c_names = "Not listed"

    return (
        f"The latest free exhibition: {top_exhibition.name}; Theme: {top_exhibition.theme}; "
        f"Curators: {c_names}."
    )


def update_exhibition(exhibition_name: str):
    try:
        ex = Exhibition.objects.get(name=exhibition_name)
    except Exhibition.DoesNotExist:
        return "No such exhibition."

    if not ex.is_free_entry:
        ex.is_free_entry = True
        ex.save()

    museum_visitors = 0
    if ex.museum:
        ex.museum.annual_visitors = F('annual_visitors') + 20000
        ex.museum.save()
        ex.museum.refresh_from_db()
        museum_visitors = ex.museum.annual_visitors

    curators = ex.curators.all()
    total_experience = 0
    if curators.exists():
        for curator in curators:
            curator.experience_years = F('experience_years') + 1
            curator.save()
        for curator in curators:
            curator.refresh_from_db()
            total_experience += curator.experience_years

    return (
        f"Updated data for {exhibition_name}: {museum_visitors} museum visitors; "
        f"{total_experience} years of curators total experience."
    )

