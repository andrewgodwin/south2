"""
This package installs monkey-patches into the currently loaded copy of Django.
They're designed to make it enough like 1.7 (things like Field.deconstruct()
and a mutable AppCache) that migrations code can run.

Just importing the module is enough to trigger them, as they're done as
decorators.
"""


from django.utils.importlib import import_module


def add_to_module(module_path, name=None, thing=None):
    """
    Decorator for functions which adds the function into the module,
    replacing anything named the same. Call with a second argument to
    patch a class in instead (or a function as a value).
    """
    def decorator(func):
        module = import_module(module_path)
        setattr(module, name or func.__name__, func)
        return func
    if thing is None:
        return decorator
    else:
        decorator(thing)


def add_to_class(class_path, name=None, thing=None):
    """
    Decorator for functions which adds the function onto a class,
    replacing anything named the same.
    """
    def decorator(func):
        module_path, class_name = class_path.rsplit(".", 1)
        module = import_module(module_path)
        klass = getattr(module, class_name)
        setattr(klass, name or func.__name__, func)
        return func
    if thing is None:
        return decorator
    else:
        decorator(thing)


# Now load patches in. They'll be importing this file for the decorators,
# but that's fine, as they're already declared.

# 1.4 - 1.6 patches
patches = [
    "model_options",
    "signals",
    "meta_app_cache",
    "app_cache_methods",
    "global_settings",
    "schema_editor",
    "database_features",
    "fields",
    "termcolors",
    "routers",
]

# 1.4 only patches
import django
if django.VERSION[1] == 4:
    patches += [
        "django_1_4",
    ]

# 1.4 and 1.5 patches
import django
if django.VERSION[1] < 6:
    patches += [
        "atomic",
    ]

for patch in patches:
    import_module("south.patches.%s" % patch)

# Finally make south appear as django.db.migrations for
# the imports in migrations to work (these are all of the form
# 'from django.db import migrations', so they don't care that
# it's not a true submodule).

import django.db
import south.migrations
django.db.migrations = south.migrations
