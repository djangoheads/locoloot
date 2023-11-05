from django.db import models


class SpaceLanguage(models.Model):
    space = models.ForeignKey(
        "Space", on_delete=models.CASCADE, related_name="languages"
    )
    language = models.ForeignKey(
        "languages_plus.Language",
        on_delete=models.CASCADE,
        related_name="space_languages",
    )

    class Meta:
        unique_together = (("space", "language"),)

    def __str__(self):
        return f"{self.space} - {self.language}"
