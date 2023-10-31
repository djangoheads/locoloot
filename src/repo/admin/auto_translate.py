from django.contrib import admin

from .. import models


@admin.register(models.AutoTranslate)
class AutoTranslateAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    autocomplete_fields = ["engine", "group", "from_language", "to_language"]
