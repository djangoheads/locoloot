from django.db import models
from django.db.models import F


class KeyGroup(models.Model):
    class Meta:
        unique_together = (("key", "group"),)

    key = models.ForeignKey("Key", on_delete=models.CASCADE, related_name="groups")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="keys")

    def __str__(self):
        return f"{self.group.name}"

    def get_phrases(self, language, fallback_language):
        return self.phrases.filter(language=language)
