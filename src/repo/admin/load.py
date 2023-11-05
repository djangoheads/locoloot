from django.contrib import admin

from .. import models


@admin.register(models.ImportI18Next)
class ImportI18NextAdmin(admin.ModelAdmin):
    autocomplete_fields = ["space", "group", "language"]
