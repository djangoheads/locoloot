from django.contrib import admin
from django.db.models import Count

from .. import models


class PhraseInlineAdmin(admin.StackedInline):
    model = models.Phrase
    template = "admin/edit_inline/repo_stacked.html"
    autocomplete_fields = ["language"]
    readonly_fields = ["auto_translated", "language", "source_value", "value"]
    show_change_link = True
    extra = 1
    fieldsets = [
        (None, {"fields": [("language", "auto_translated"),],},),
        (
            None,
            {"classes": ["wide", "extrapretty"], "fields": ["source_value", "value"],},
        ),
    ]


@admin.register(models.Key)
class KeyAdmin(admin.ModelAdmin):
    search_fields = ["key_index__startswith"]
    list_filter = ["space", "groups__group"]
    inlines = [PhraseInlineAdmin]

    list_display = ["get_key", "phrases_count"]

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related("groups__group")
        qs = qs.annotate(phrases_count=Count("phrases"))
        return qs

    @admin.display(description="Phrases", ordering="phrases_count")
    def phrases_count(self, obj):
        return obj.phrases_count

    @admin.display(description="Key", ordering="key")
    def get_key(self, obj):
        return obj.key[:50] + "..." if len(obj.key) > 50 else obj.key
