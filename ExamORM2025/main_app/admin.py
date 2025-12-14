from django.contrib import admin

from .models import Museum, Curator, Exhibition
from .helper import UpdatedAtReadOnlyAdminMixin


@admin.register(Museum)
class MuseumAdmin(UpdatedAtReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'location', 'annual_visitors')
    list_filter = ('annual_visitors',)
    search_fields = ('name',)


@admin.register(Curator)
class CuratorAdmin(UpdatedAtReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience_years')
    list_filter = ('experience_years',)
    search_fields = ('name', 'specialization')


@admin.register(Exhibition)
class ExhibitionAdmin(UpdatedAtReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'theme', 'opening_date', 'is_free_entry', 'details', 'museum')
    list_filter = ('is_free_entry', 'theme')
    search_fields = ('name', 'museum__name')

