from django.db import models


class Phrase(models.Model):
    class Meta:
        unique_together = (("language", "key"),)

    language = models.ForeignKey(
        "languages_plus.Language", on_delete=models.CASCADE, related_name="phrases"
    )
    key = models.ForeignKey("Key", on_delete=models.CASCADE, related_name="phrases")
    value = models.TextField(blank=True, null=True)
    auto_translated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.key} ({self.language.iso_639_1})"

    @property
    def source(self):
        return self.key.phrases.filter(language__iso_639_1="en").first()

    @property
    def source_value(self):
        return self.source.value if self.source else ""
