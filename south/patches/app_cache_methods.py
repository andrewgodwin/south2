from south.patches import add_to_class


@add_to_class("django.db.models.loading.AppCache")
def get_app_configs(self, only_with_models_module=False):
    """
    Emulates the 1.7 app configs just enough so you can iterate over
    them and get app info.
    """
    configs = []
    for app in self.get_apps():
        configs.append(self.get_app_config(app.__name__.split('.')[-2]))
    return configs


@add_to_class("django.db.models.loading.AppCache")
def get_app_config(self, app_label, only_installed=True, only_with_models_module=False):
    """
    Emulates the 1.7 app configs just enough so you can get info
    from them.
    """
    app = self.get_app(app_label)
    config_class = type("AppConfig", (object, ), {})
    config = config_class()
    config.name = app.__name__.rsplit(".", 1)[0]
    config.label = app.__name__.split('.')[-2]
    config.models_module = app
    return config
