import hashlib

from django.db import models
from django.db.models import Case, Subquery, OuterRef, F, When, Value
from django.dispatch import receiver
from languages_plus.models import Language


class KeyQuerySet(models.QuerySet):
    def translate(self, language, fallback_language):
        from ..models import Phrase

        return self.annotate(
            translation=Subquery(
                Phrase.objects.filter(key=OuterRef("id"), language=language).values(
                    "value"
                )[:1],
                output_field=models.TextField(),
            ),
            fallback_translation=Subquery(
                Phrase.objects.filter(
                    key=OuterRef("id"), language=fallback_language
                ).values("value")[:1],
                output_field=models.TextField(),
            ),
        )


class Key(models.Model):
    class Meta:
        unique_together = (("space", "key_hash"),)

    space = models.ForeignKey("Space", on_delete=models.CASCADE, related_name="keys")
    key = models.TextField()
    key_hash = models.CharField(max_length=64, db_index=True, editable=False)
    key_index = models.CharField(max_length=255, db_index=True, editable=False, null=True)

    objects = KeyQuerySet.as_manager()

    def __str__(self):
        return f"{self.key}"

    def save(self, *args, **kwargs):
        print(locals())
        self.key_hash = hashlib.sha256(self.key.encode()).hexdigest()
        self.key_index = self.key[:255]
        return super().save(*args, **kwargs)

    def translate(self, engine, from_language, to_language, skip_translated=False):
        from_phrase = self.phrases.filter(language__iso_639_1=from_language).first()
        if not from_phrase:
            print("Skip: Phrase is not translated to source language")
            return

        if self.phrases.filter(
            language__iso_639_1=to_language, auto_translated=False
        ).exists():
            print("Skip: Phrase is translated manually, can't translate automatically")
            return

        if (
            skip_translated
            and self.phrases.filter(language__iso_639_1=to_language).exists()
        ):
            print(
                "Skip: Phrase is translated, and skipped because of --skip-translated flag"
            )
            return

        translated_text = engine.translate(
            from_phrase.value, from_language, to_language
        )
        self.phrases.update_or_create(
            language=Language.objects.get(iso_639_1=to_language),
            defaults={"value": translated_text, "auto_translated": True,},
        )
