from django.db import models
from django.db.models import When, F, Subquery, Case, Value, OuterRef


class Group(models.Model):
    class Meta:
        ordering = ("space", "name")

    space = models.ForeignKey("Space", on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"{self.name}"

    def get_translation(self, language, fallback_language: str = None):
        """
        TODO: Optimize this query. The part for fallback language is not efficient
        """
        from ..models import Key

        return Key.objects.filter(groups__group=self).translate(
            language, fallback_language
        )
