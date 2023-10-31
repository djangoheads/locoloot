import dynaconf  # noqa

settings = dynaconf.DjangoDynaconf(
    __name__,
    settings_files=["/home/app/config/settings.yaml"],
    merge_enabled=True,
)  # noqa
