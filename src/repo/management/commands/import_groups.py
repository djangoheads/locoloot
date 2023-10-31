import os

from django.core.management import BaseCommand

from repo import models


class Command(BaseCommand):
    help = "Inited components from json files "

    def add_arguments(self, parser):
        parser.add_argument("space-name", type=str)
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        path = options["path"]
        space_name = options["space-name"]
        for filename in os.listdir(path):
            if not os.path.isfile(os.path.join(path, filename)):
                continue
            name = filename.split(".")[0]
            models.Group.objects.get_or_create(
                name=name, space=models.Space.objects.get(name=space_name)
            )
            print(f"Creating group {name} in {space_name}")
