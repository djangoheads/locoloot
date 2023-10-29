from django.contrib import admin
from django.utils.safestring import mark_safe

from .. import models


@admin.register(models.Phrase)
class PhraseAdmin(admin.ModelAdmin):
    readonly_fields = ["key", "language"]
    search_fields = ["key__key", "value"]

    list_filter = ["auto_translated", "key__space", "language"]
    list_display = ["source_value", "value"]
    list_select_related = ["key", "language"]
    list_editable = [
        "value",
    ]

    fields = ["auto_translated", "language", "value", "get_source_value", "key"]
    readonly_fields = ["get_source_value", "key"]
    # list_display_links = ["get_key"]

    @admin.display(description="Auto", ordering="auto_translated", boolean=True)
    def get_auto_translated(self, obj):
        return obj.auto_translated

    @admin.display(description="Source value [en]", ordering="value")
    def get_source_value(self, obj):
        style = """<style>
pre {
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}</style>"""
        return mark_safe(f"{style}<pre class='flex-container'>{obj.source_value}</pre>")

    @admin.display(description="Value", ordering="value")
    def get_value(self, obj):
        return obj.value[:50] + "..." if len(obj.value) > 50 else obj.value

    @admin.display(description="Key", ordering="key__key")
    def get_key(self, obj):
        return obj.key.key[:50] + "..." if len(obj.key.key) > 50 else obj.key.key

    def save_form(self, request, form, change):
        old_value = models.Phrase.objects.get(pk=form.instance.pk).value
        new_value = form.instance.value
        if old_value != new_value:
            form.instance.auto_translated = False
        return super().save_form(request, form, change)
