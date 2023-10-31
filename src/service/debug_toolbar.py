from django.conf import settings


def show_toolbar(*args, **kwargs):
    return settings.DEBUG
