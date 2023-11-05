from django.contrib import admin
from django.db.models import Count, Subquery, OuterRef, Func, F

from .. import models


@admin.register(models.Space)
class SpaceAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    autocomplete_fields = ["default_language"]
    list_display = [
        "name",
        "groups_count",
        "keys_count",
        "phrases_count",
        "languages_count",
        "translated_count",
    ]
    list_select_related = ["owner", "default_language"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(owner=request.user)

        # See:
        # https://stackoverflow.com/questions/42543978/django-1-11-annotating-a-subquery-aggregate/69020732#69020732
        groups_count = (
            models.Group.objects.filter(space=OuterRef("id"))
            .order_by()
            .annotate(count=Func(F("id"), function="Count"))
            .values("count")
        )

        qs = qs.annotate(
            groups_count=Subquery(groups_count),
            phrases_count=Count("keys__phrases", distinct=True),
            keys_count=Count("keys", distinct=True),
        )
        return qs

    @admin.display(description="Groups", ordering="groups_count")
    def groups_count(self, obj):
        return obj.groups_count

    @admin.display(description="Keys", ordering="keys_count")
    def keys_count(self, obj):
        return obj.keys_count

    @admin.display(description="Phrases", ordering="phrases_count")
    def phrases_count(self, obj):
        return obj.phrases_count

    @admin.display(description="Trans/Total")
    def translated_count(self, obj):
        translated = obj.phrases_count
        untranslated = obj.languages_count * obj.keys_count
        return f"{translated}/{untranslated}"
