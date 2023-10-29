from django.db import models


class Space(models.Model):
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="spaces"
    )
    name = models.CharField(max_length=255, unique=True)
    default_language = models.ForeignKey(
        "languages_plus.Language", on_delete=models.CASCADE, related_name="+"
    )

    def __str__(self):
        return self.name + f" [{self.default_language.iso_639_1}]"

    @property
    def languages_count(self):
        from .. models import Phrase
        return Phrase.objects.filter(key__space=self).aggregate(
            languages_count=models.Count('language', distinct=True)
        )['languages_count']
