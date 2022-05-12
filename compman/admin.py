from django.contrib import admin

from compman.models import Player


@admin.decorators.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    sortable_by = ['name']
    list_filter = ['name']


# Register your models here.
