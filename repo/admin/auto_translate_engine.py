from django.contrib import admin
from django.utils.safestring import mark_safe
from translators.server import tss

from .. import models


@admin.register(models.AutoTranslateEngine)
class AutoTranslateEngineAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["config_doc"]

    def config_doc(self, instance: models.AutoTranslateEngine):
        doc = str(getattr(getattr(tss, instance.engine), "__doc__"))
        if not doc:
            return
        doc = doc.split(":param **kwargs:")
        if len(doc) < 1:
            return

        doc: str = doc[1]

        kv = []
        for line in doc.splitlines():
            line = line.strip()
            if line.startswith(":param"):
                kv.append(line[7:].split(":", 1))

        result = ""
        for key, value in kv:
            result += (
                f"<tr>"
                f"<td><strong><pre>{key}:</pre></strong></td>"
                f"<td><pre>{value}</pre></td>"
                f"</tr>"
            )

        return mark_safe(f"<table>{result}</table>")
