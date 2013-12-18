from django.db.models.fields import NOT_PROVIDED, Field, AutoField, BooleanField, DateField, DecimalField, EmailField, FilePathField, IPAddressField, GenericIPAddressField, NullBooleanField, SlugField, TimeField, URLField
from django.db.models.fields.related import CASCADE, ForeignKey, OneToOneField, ManyToManyField
from django.utils import six
from django.conf import settings
from south.patches import add_to_class


@add_to_class("django.db.models.fields.Field")
def db_parameters(self, connection):
    db_type = self.db_type(connection)
    if " CHECK " in db_type:
        bits = db_type.split(" CHECK ", 1)
        return {
            "type": bits[0],
            "check": bits[1],
        }
    else:
        return {
            "type": db_type,
            "check": None,
        }


Field.old_init = Field.__init__

@add_to_class("django.db.models.fields.Field")
def __init__(self, *args, **kwargs):
    self._validators = kwargs.get("validators", [])
    self._error_messages = kwargs.get("error_messages", None)
    self._verbose_name = kwargs.get("verbose_name", None if len(args) == 0 else args[0])
    self.old_init(*args, **kwargs)


@add_to_class("django.db.models.fields.Field")
def deconstruct(self):
    # Original code below
    keywords = {}
    possibles = {
        "verbose_name": None,
        "primary_key": False,
        "max_length": None,
        "unique": False,
        "blank": False,
        "null": False,
        "db_index": False,
        "default": NOT_PROVIDED,
        "editable": True,
        "serialize": True,
        "unique_for_date": None,
        "unique_for_month": None,
        "unique_for_year": None,
        "choices": [],
        "help_text": '',
        "db_column": None,
        "db_tablespace": settings.DEFAULT_INDEX_TABLESPACE,
        "auto_created": False,
        "validators": [],
        "error_messages": None,
    }
    attr_overrides = {
        "unique": "_unique",
        "choices": "_choices",
        "error_messages": "_error_messages",
        "validators": "_validators",
        "verbose_name": "_verbose_name",
    }
    equals_comparison = set(["choices", "validators", "db_tablespace"])
    for name, default in possibles.items():
        value = getattr(self, attr_overrides.get(name, name))
        if name in equals_comparison:
            if value != default:
                keywords[name] = value
        else:
            if value is not default:
                keywords[name] = value
    # Work out path - we shorten it for known Django core fields
    path = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
    if path.startswith("django.db.models.fields.related"):
        path = path.replace("django.db.models.fields.related", "django.db.models")
    if path.startswith("django.db.models.fields.files"):
        path = path.replace("django.db.models.fields.files", "django.db.models")
    if path.startswith("django.db.models.fields.proxy"):
        path = path.replace("django.db.models.fields.proxy", "django.db.models")
    if path.startswith("django.db.models.fields"):
        path = path.replace("django.db.models.fields", "django.db.models")
    # Return basic info - other fields should override this.
    return (
        self.name,
        path,
        [],
        keywords,
    )


@add_to_class("django.db.models.fields.AutoField")
def deconstruct(self):
    name, path, args, kwargs = super(AutoField, self).deconstruct()
    del kwargs['blank']
    kwargs['primary_key'] = True
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.BooleanField")
def deconstruct(self):
    name, path, args, kwargs = super(BooleanField, self).deconstruct()
    del kwargs['blank']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.DateField")
def deconstruct(self):
    name, path, args, kwargs = super(DateField, self).deconstruct()
    if self.auto_now:
        kwargs['auto_now'] = True
        del kwargs['editable']
        del kwargs['blank']
    if self.auto_now_add:
        kwargs['auto_now_add'] = True
        del kwargs['editable']
        del kwargs['blank']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.DecimalField")
def deconstruct(self):
    name, path, args, kwargs = super(DecimalField, self).deconstruct()
    if self.max_digits:
        kwargs['max_digits'] = self.max_digits
    if self.decimal_places:
        kwargs['decimal_places'] = self.decimal_places
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.EmailField")
def deconstruct(self):
    name, path, args, kwargs = super(EmailField, self).deconstruct()
    # We do not exclude max_length if it matches default as we want to change
    # the default in future.
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.FilePathField")
def deconstruct(self):
    name, path, args, kwargs = super(FilePathField, self).deconstruct()
    if self.path != '':
        kwargs['path'] = self.path
    if self.match is not None:
        kwargs['match'] = self.match
    if self.recursive is not False:
        kwargs['recursive'] = self.recursive
    if self.allow_files is not True:
        kwargs['allow_files'] = self.allow_files
    if self.allow_folders is not False:
        kwargs['allow_folders'] = self.allow_folders
    if kwargs.get("max_length", None) == 100:
        del kwargs["max_length"]
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.IPAddressField")
def deconstruct(self):
    name, path, args, kwargs = super(IPAddressField, self).deconstruct()
    del kwargs['max_length']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.GenericIPAddressField")
def deconstruct(self):
    name, path, args, kwargs = super(GenericIPAddressField, self).deconstruct()
    if self.unpack_ipv4 is not False:
        kwargs['unpack_ipv4'] = self.unpack_ipv4
    if self.protocol != "both":
        kwargs['protocol'] = self.protocol
    if kwargs.get("max_length", None) == 39:
        del kwargs['max_length']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.NullBooleanField")
def deconstruct(self):
    name, path, args, kwargs = super(NullBooleanField, self).deconstruct()
    del kwargs['null']
    del kwargs['blank']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.SlugField")
def deconstruct(self):
    name, path, args, kwargs = super(SlugField, self).deconstruct()
    if kwargs.get("max_length", None) == 50:
        del kwargs['max_length']
    if self.db_index is False:
        kwargs['db_index'] = False
    else:
        del kwargs['db_index']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.TimeField")
def deconstruct(self):
    name, path, args, kwargs = super(TimeField, self).deconstruct()
    if self.auto_now is not False:
        kwargs["auto_now"] = self.auto_now
    if self.auto_now_add is not False:
        kwargs["auto_now_add"] = self.auto_now_add
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.URLField")
def deconstruct(self):
    name, path, args, kwargs = super(URLField, self).deconstruct()
    if kwargs.get("max_length", None) == 200:
        del kwargs['max_length']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.related.ForeignKey")
def deconstruct(self):
    name, path, args, kwargs = super(ForeignKey, self).deconstruct()
    if isinstance(self.rel.to, six.string_types):
        kwargs['to'] = self.rel.to
    else:
        kwargs['to'] = "%s.%s" % (self.rel.to._meta.app_label, self.rel.to._meta.object_name)
    # Handle the simpler arguments
    if self.db_index:
        del kwargs['db_index']
    else:
        kwargs['db_index'] = False
    if getattr(self, "db_constraint", True) is not True:
        kwargs['db_constraint'] = self.db_constraint
    if self.rel.on_delete is not CASCADE:
        kwargs['on_delete'] = self.rel.on_delete
    # Rel needs more work.
    if self.rel.field_name:
        kwargs['to_field'] = self.rel.field_name
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.related.OneToOneField")
def deconstruct(self):
    name, path, args, kwargs = super(OneToOneField, self).deconstruct()
    if "unique" in kwargs:
        del kwargs['unique']
    return name, path, args, kwargs


@add_to_class("django.db.models.fields.related.ManyToManyField")
def deconstruct(self):
    name, path, args, kwargs = super(ManyToManyField, self).deconstruct()
    if isinstance(self.rel.to, six.string_types):
        kwargs['to'] = self.rel.to
    else:
        kwargs['to'] = "%s.%s" % (self.rel.to._meta.app_label, self.rel.to._meta.object_name)
    # Handle the simpler arguments
    if getattr(self.rel, "db_constraint", True) is not True:
        kwargs['db_constraint'] = self.rel.db_constraint
    if "help_text" in kwargs:
        del kwargs['help_text']
    # Rel needs more work.
    if isinstance(self.rel.to, six.string_types):
        kwargs['to'] = self.rel.to
    else:
        kwargs['to'] = "%s.%s" % (self.rel.to._meta.app_label, self.rel.to._meta.object_name)
    return name, path, args, kwargs
