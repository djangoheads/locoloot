import time
import translators

from django.db import models
from translators.server import TranslatorError


ENGINE_CHOICES = [(engine, engine) for engine in translators.translators_pool]


class AutoTranslateEngine(models.Model):
    name = models.CharField(max_length=255)
    engine = models.CharField(max_length=255, choices=ENGINE_CHOICES)
    config = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.engine})"

    def translate(self, value, from_language, to_language):
        """
        TODO: Refactor, reduce complexity
        TODO: Fix RTL languages
        """
        tries = 0
        max_tries = 3
        timeout_factor = 0.5

        def parse_template_tags(sub_value):
            """
            TODO: FIX RTL languages
            """
            if "{{" not in sub_value:
                return sub_value

            result = ""
            for part in sub_value.split("{{"):
                if "}}" not in part:
                    result += self.translate(part, from_language, to_language)
                    if part.startswith(" "):
                        result = " " + result
                    if part.endswith(" "):
                        result += " "
                    continue

                part = part.split("}}")
                result += "{{" + part[0] + "}}"
                result += self.translate(part[1], from_language, to_language)

            return result.strip()

        if "{{" in value:
            return parse_template_tags(value)

        while tries < max_tries:
            timeout = timeout_factor + timeout_factor * tries
            try:
                return translators.translate_text(
                    value,
                    translator=self.engine,
                    from_language=from_language,
                    to_language=to_language,
                    **self.config,
                )
            except TranslatorError:
                raise
            except Exception as e:
                print(f"Error during translation with {self.engine}, {to_language}, sleeping for {timeout}, {tries}/{max_tries} try")
                time.sleep(timeout)
                tries += 1
                if tries == max_tries:
                    try:
                        result = translators.translate_text(
                            value,
                            translator=self.engine,
                            from_language=from_language,
                            to_language=to_language,
                            **dict(self.config, is_detail_result=True),
                        )
                    except TranslatorError:
                        result = "Undefined"
                    raise Exception(f"Failed to translate: {e} with {result}") from e
