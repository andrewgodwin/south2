from south.patches import add_to_class
from django.core.exceptions import ImproperlyConfigured


try:
    @add_to_class("django.db.backends.postgresql_psycopg2.base.DatabaseWrapper")
    def schema_editor(self, *args, **kwargs):
        from south.schema.postgresql import DatabaseSchemaEditor
        return DatabaseSchemaEditor(self, *args, **kwargs)
except ImproperlyConfigured:
    pass


try:
    @add_to_class("django.db.backends.mysql.base.DatabaseWrapper")
    def schema_editor(self, *args, **kwargs):
        from south.schema.mysql import DatabaseSchemaEditor
        return DatabaseSchemaEditor(self, *args, **kwargs)
except ImproperlyConfigured:
    pass


try:
    @add_to_class("django.db.backends.sqlite3.base.DatabaseWrapper")
    def schema_editor(self, *args, **kwargs):
        from south.schema.sqlite3 import DatabaseSchemaEditor
        return DatabaseSchemaEditor(self, *args, **kwargs)
except ImproperlyConfigured:
    pass


try:
    @add_to_class("django.db.backends.oracle.base.DatabaseWrapper")
    def schema_editor(self, *args, **kwargs):
        from south.schema.oracle import DatabaseSchemaEditor
        return DatabaseSchemaEditor(self, *args, **kwargs)
except ImproperlyConfigured:
    pass
