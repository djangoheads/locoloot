import json
import typing

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pydantic import RootModel

from repo.models import Key, Group


class FileImport(models.Model):
    class Meta:
        abstract = True

    space = models.ForeignKey("Space", on_delete=models.CASCADE, related_name="imports")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="+")
    language = models.ForeignKey(
        "languages_plus.Language",
        default="en",
        on_delete=models.CASCADE,
        related_name="+",
    )
    file = models.FileField(upload_to="imports/%Y/%m/%d/")

    def __str__(self):
        group_name = self.group.name if self.group else "No Group"
        return f"{self.space.name} / {group_name} / {self.language.name}"

    @classmethod
    def from_file(cls, space, group_name, language, file):
        data = json.load(file)
        if not data:
            return
        data = [("", I18NextSchema(**data).model_dump())]

        result = {}

        def key_collector(value, path=""):
            for key, value in value.items():
                if isinstance(value, dict):
                    data.append((key, value))
                else:
                    result[f"{path}{'.' if path else ''}{key}"] = value

        while data:
            path, to_parse = data.pop()
            key_collector(to_parse, path=path)

        group, created = Group.objects.get_or_create(name=group_name, space=space)
        for key, value in result.items():
            key, created = Key.objects.get_or_create(space=space, key=key)
            key.groups.update_or_create(group=group)
            key.phrases.update_or_create(language=language, defaults={"value": value})


class ImportI18Next(FileImport):
    pass


class I18NextComponentSchema(RootModel[typing.Dict[str, str]]):
    pass


class I18NextSchema(RootModel[typing.Dict[str, str | I18NextComponentSchema]]):
    pass


@receiver(post_save, sender=ImportI18Next)
def import_i18next(sender, instance, created, **kwargs):
    instance.from_file(instance.space, instance.group, instance.language, instance.file)
