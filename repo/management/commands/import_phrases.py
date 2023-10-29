import os

from django.core.management import BaseCommand
from languages_plus.models import Language

from repo import models
from repo.models.load import FileImport


class Command(BaseCommand):
    help = "Inited components from json files "

    def add_arguments(self, parser):
        parser.add_argument("space-name", type=str)
        parser.add_argument("locale-root", type=str)

    def handle(self, *args, **options):
        locale_root = options["locale-root"]
        space_name = options["space-name"]
        languages = []
        for dirname in os.listdir(locale_root):
            if not os.path.isdir(os.path.join(locale_root, dirname)):
                continue
            language = Language.objects.filter(pk=dirname).first()
            if not language:
                print(f"{dirname} is not registered in LocoLoot")
                continue

            languages.append(dirname)

        total = 0
        processed = 0
        for language in languages:
            language = Language.objects.get(pk=language)
            for group in models.Group.objects.filter(space__name=space_name):
                filename = os.path.join(
                    locale_root, language.iso_639_1, f"{group.name}.json"
                )
                total += 1
                if not os.path.exists(filename):
                    print(
                        f"{filename} does not exist, {group} group does not have translations for {language}"
                    )
                    continue

                with open(filename, "r") as h:
                    try:
                        FileImport.from_file(
                            space=group.space,
                            group_name=group.name,
                            language=language,
                            file=h,
                        )
                        processed += 1
                    except Exception as e:
                        print(
                            f"Error while importing {group} group for {language} ({filename}):\n{e}"
                        )
                        continue

        print(f"Processed {processed} out of {total} files")
        # for group in models.Group.objects.all():
        #     for key in models.Key.objects.filter(groups__group=group):
        #         key.get_translation(options["language"])
