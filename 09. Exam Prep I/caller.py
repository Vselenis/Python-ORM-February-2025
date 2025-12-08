import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    do = Director.objects.all()

    if search_name is not None and search_nationality is not None:
        do = do.filter(
            Q(full_name__icontains=search_name),
            Q(nationality__icontains=search_nationality),
        )

    elif search_name is not None:
        do = do.filter(full_name__icontains=search_name)

    elif search_nationality is not None:
        do = do.filter(nationality__icontains=search_nationality)

    do = do.order_by("full_name")

    if not do.exists():
        return ""

    result_lines = [
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        for d in do
    ]

    return "\n".join(result_lines)


def get_top_director():
    do = Director.objects.get_directors_by_movies_count()

    if not do.exists():
        return ""

    top = do.first()

    return f"Top Director: {top.full_name}, movies: {top.movie_count}."


def get_top_actor():
    ao = Actor.objects.annotate(
        starring_count=Count("starred_movies"),
    ).filter(starring_count__gt=0)

    if not ao.exists():
        return ""

    ao = ao.order_by("-starring_count", "full_name")

    top = ao.first()

    movies_qs = top.starred_movies.order_by("title")

    if not movies_qs.exists():
        return ""

    movie_titles = [m.title for m in movies_qs]

    avg_rating = movies_qs.aggregate(avg=Avg("rating"))["avg"]

    avg_rating_str = f"{avg_rating:.1f}"

    titles_str = ", ".join(movie_titles)

    return (
        f"Top Actor: {top.full_name}, starring in movies: {titles_str}, "
        f"movies average rating: {avg_rating_str}"
    )

def get_actors_by_movies_count():
    qs = Actor.objects.annotate(
        movies_count=Count("movies")
    ).filter(movies_count__gt=0)

    if not qs.exists():
        return ""

    qs = qs.order_by("-movies_count", "full_name")
    top_three = qs[:3]

    lines = [
        f"{actor.full_name}, participated in {actor.movies_count} movies"
        for actor in top_three
    ]

    return "\n".join(lines)


def get_top_rated_awarded_movie():
    qs = Movie.objects.filter(is_awarded=True)

    if not qs.exists():
        return ""

    qs = qs.order_by("-rating", "title")
    movie = qs.first()
    rating_str = f"{movie.rating:.1f}"

    if movie.starring_actor:
        starring_name = movie.starring_actor.full_name
    else:
        starring_name = "N/A"

    cast_qs = movie.actors.order_by("full_name")

    cast_names = ", ".join(a.full_name for a in cast_qs)

    return (
        f"Top rated awarded movie: {movie.title}, rating: {rating_str}. "
        f"Starring actor: {starring_name}. "
        f"Cast: {cast_names}."
    )


def increase_rating():
    ir = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not ir.exists():
        return "No ratings increased."
    updated = 0

    for movie in ir:
        new_rating = float(movie.rating) + 0.1
        if new_rating > 10.0:
            new_rating = 10.0

        if new_rating != float(movie.rating):
            movie.rating = new_rating
            movie.save()
            updated += 1

    if updated == 0:
        return "No ratings increased."

    return f"Rating increased for {updated} movies."
