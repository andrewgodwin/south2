from south.patches import add_to_module
from django.dispatch import Signal
from django.db.models import signals


add_to_module(
    "django.db.models.signals",
    "pre_migrate",
    Signal(providing_args=["app", "create_models", "verbosity", "interactive", "db"]),
)

add_to_module(
    "django.db.models.signals",
    "post_migrate",
    Signal(providing_args=["class", "app", "created_models", "verbosity", "interactive", "db"])
)


@add_to_module("django.core.management.sql")
def emit_pre_migrate_signal(create_models, verbosity, interactive, db):
    # Emit the pre_migrate signal for every application.
    from south.app_cache import app_cache
    for app in app_cache.get_apps():
        app_name = app.__name__.split('.')[-2]
        if verbosity >= 2:
            print("Running pre-migrate handlers for application %s" % app_name)
        signals.pre_migrate.send(
            sender=app,
            app=app,
            create_models=create_models,
            verbosity=verbosity,
            interactive=interactive,
            db=db,
        )


@add_to_module("django.core.management.sql")
def emit_post_migrate_signal(created_models, verbosity, interactive, db):
    # Emit the post_migrate signal for every application.
    from south.app_cache import app_cache
    for app in app_cache.get_apps():
        app_name = app.__name__.split('.')[-2]
        if verbosity >= 2:
            print("Running post-migrate handlers for application %s" % app_name)
        signals.post_migrate.send(
            sender=app,
            app=app,
            created_models=created_models,
            verbosity=verbosity,
            interactive=interactive,
            db=db,
        )
