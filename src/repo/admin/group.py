from django.contrib import admin
from django.db.models import OuterRef, Subquery, Count, Func, F
from languages_plus.models import Language

from .. import models


class KeyGroupsInlineAdmin(admin.TabularInline):
    template = "admin/edit_inline/repo_tabular.html"
    model = models.KeyGroup
    autocomplete_fields = ["key"]
    readonly_fields = ["key"]
    extra = 0


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = ["name", "space", "keys_count"]
    inlines = [KeyGroupsInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(keys_count=Count("keys", distinct=True),)
        return qs

    @admin.display(description="Keys", ordering="keys_count")
    def keys_count(self, obj):
        return obj.keys_count
