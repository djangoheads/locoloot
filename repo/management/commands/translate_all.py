import os

from django.core.management import BaseCommand
from languages_plus.models import Language

from repo import models
from repo.models.load import FileImport


class Command(BaseCommand):
    help = "Inited components from json files "

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-translated", action="store_true", help="Skip All Translated"
        )
        parser.add_argument(
            "--engine", nargs="+", type=str, help="Engine IDs to use by priority"
        )
        parser.add_argument(
            "--skip-language", nargs="+", type=str, help="Skip Languages"
        )
        parser.add_argument("--space-name", type=str)

    def handle(self, *args, **options):
        print("Starting translation:")
        for op in options:
            print(f"{op}: {options[op]}")

        engines_conf = options["engine"]
        engines = models.AutoTranslateEngine.objects.filter(pk__in=engines_conf)
        engines = {str(engine.pk): engine for engine in engines}
        space = models.Space.objects.get(name=options["space_name"])
        skip_translated = options.get("skip_translated") or False
        skip_languages = options.get("skip_language") or []

        languages = set()

        for phrase in models.Phrase.objects.filter(key__space=space):
            languages.add(phrase.language.iso_639_1)

        languages = sorted(languages)
        print(f"Languages: {', '.join(languages)}")

        for language in languages:
            if language == "en":
                continue
            if language in skip_languages:
                print(f"Skipped: {language} because of --skip-language flag")
                continue
            for key in models.Key.objects.filter(space=space):
                for engine_id in engines_conf:
                    engine = engines[engine_id]
                    usage = "Using:" if engine_id == engines_conf[0] else "Switched to:"
                    try:
                        key.translate(
                            engine, "en", language, skip_translated=skip_translated,
                        )
                        print(f"{usage} engine: {engine}")
                        print(f"Translated {key} to {language}")
                        break
                    except Exception as e:
                        print(f"[{engine}] Error translating {key} to {language}: {e}")
