from django.db.models import options
from south.patches import add_to_module, add_to_class


options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("app_cache", )


@add_to_module("django.db.models.options")
def normalize_unique_together(unique_together):
    """
    unique_together can be either a tuple of tuples, or a single
    tuple of two strings. Normalize it to a tuple of tuples, so that
    calling code can uniformly expect that.
    """
    if not unique_together:
        return ()
    first_element = next(iter(unique_together))
    if not isinstance(first_element, (tuple, list)):
        unique_together = (unique_together,)
    # Normalize everything to tuples
    return tuple(tuple(ut) for ut in unique_together)


options.Options.old_init = options.Options.__init__
@add_to_class("django.db.models.options.Options")
def __init__(self, *args, **kwargs):
    from south.app_cache import app_cache
    self.app_cache = app_cache
    self.old_init(*args, **kwargs)


options.Options.old_contribute_to_class = options.Options.contribute_to_class
@add_to_class("django.db.models.options.Options")
def contribute_to_class(self, cls, name):
    self.original_attrs = {}
    if self.meta:
        meta_attrs = self.meta.__dict__.copy()
        for attr_name in options.DEFAULT_NAMES:
            if attr_name in meta_attrs:
                self.original_attrs[attr_name] = getattr(self, attr_name)
            elif hasattr(self.meta, attr_name):
                self.original_attrs[attr_name] = getattr(self, attr_name)
    return self.old_contribute_to_class(cls, name)
