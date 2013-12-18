from south.patches import add_to_class


@add_to_class("django.db.utils.ConnectionRouter")
def allow_migrate(self, db, model):
    for router in self.routers:
        try:
            try:
                method = router.allow_migrate
            except AttributeError:
                method = router.allow_syncdb
        except AttributeError:
            # If the router doesn't have a method, skip to the next one.
            pass
        else:
            allow = method(db, model)
            if allow is not None:
                return allow
    return True


@add_to_class("django.db.utils.ConnectionRouter")
def get_migratable_models(self, app, db, include_auto_created=False):
    from south.app_cache import app_cache
    return [
        model
        for model in app_cache.get_models(app, include_auto_created=include_auto_created)
        if self.allow_migrate(db, model)
    ]
