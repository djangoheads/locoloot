from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AutoTranslate(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="+")
    from_language = models.ForeignKey(
        "languages_plus.Language", on_delete=models.CASCADE, related_name="+"
    )
    to_language = models.ForeignKey(
        "languages_plus.Language", on_delete=models.CASCADE, related_name="+"
    )
    engine = models.ForeignKey(
        "AutoTranslateEngine", on_delete=models.CASCADE, related_name="+"
    )

    def __str__(self):
        return (
            f"{self.engine} / {self.group} - {self.from_language} → {self.to_language}"
        )

    def translate(self):
        for key_group in self.group.keys.all():
            key = key_group.key
            key.translate(
                self.engine, self.from_language.iso_639_1, self.to_language.iso_639_1
            )


@receiver(post_save, sender=AutoTranslate)
def auto_translate(sender, instance: AutoTranslate, created, **kwargs):
    instance.translate()


#
# def translate(value, instance):
#     tries = 0
#     timeout = 2
#
#     def parse_template_tags(value, instance):
#         if "{{" not in value:
#             return value
#
#         result = ""
#         for part in value.split("{{"):
#             if "}}" not in part:
#                 result += translate(part, instance)
#                 continue
#
#             part = part.split("}}")
#             result += "{{" + part[0] + "}}"
#             result += translate(part[1], instance)
#
#         return result
#
#     if "{{" in value:
#         print(f"{value} > {parse_template_tags(value, instance)}")
#
#     try:
#         return translators.translate_text(
#             f"{value}",
#             translator=instance.engine.engine,
#             from_language=instance.from_language.iso_639_1,
#             to_language=instance.to_language.iso_639_1,
#             **instance.engine.config
#         )
#     except Exception as e:
#         print(f"== ERROR: sleeping for {timeout}, {tries}: Try ==")
#         print(e)
#         time.sleep(2)
#         tries += 1
