from django.http import JsonResponse

from . import models


def i18next_http_interface(request, space: str, lang_code: str, namespace: str):
    """
    See: https://github.com/i18next/i18next-http-backend

    :param request:
    :return:
    """
    fallback_language = "en"
    namespace = models.Group.objects.get(space__name=space, name=namespace)
    annotated_keys = namespace.get_translation(
        language=lang_code, fallback_language=fallback_language
    )
    data = {}
    for key in annotated_keys:
        data[key.key] = key.translation or key.fallback_translation
    return JsonResponse(data)
