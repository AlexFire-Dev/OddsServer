from django.contrib import admin

from .models import OddData


@admin.register(OddData)
class OddDataAdmin(admin.ModelAdmin):
    list_display = ("game_id", "od_add_time", "stamp")
