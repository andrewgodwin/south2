from django.core.exceptions import ImproperlyConfigured

from django.db.backends import BaseDatabaseFeatures
BaseDatabaseFeatures.can_rollback_ddl = False
BaseDatabaseFeatures.supports_combined_alters = False
BaseDatabaseFeatures.max_index_name_length = 63
BaseDatabaseFeatures.supports_foreign_keys = True
BaseDatabaseFeatures.supports_check_constraints = True
BaseDatabaseFeatures.requires_literal_defaults = False
BaseDatabaseFeatures.connection_persists_old_columns = False


try:
    from django.db.backends.postgresql_psycopg2.base import DatabaseFeatures
    DatabaseFeatures.can_rollback_ddl = True
    DatabaseFeatures.supports_combined_alters = True
except ImproperlyConfigured:
    pass


try:
    from django.db.backends.mysql.base import DatabaseFeatures
    DatabaseFeatures.supports_check_constraints = False
except ImproperlyConfigured:
    pass


try:
    from django.db.backends.sqlite3.base import DatabaseFeatures
    DatabaseFeatures.supports_foreign_keys = False
    DatabaseFeatures.supports_check_constraints = False
except ImproperlyConfigured:
    pass


try:
    from django.db.backends.oracle.base import DatabaseFeatures
    DatabaseFeatures.max_index_name_length = 30
    DatabaseFeatures.requires_literal_defaults = True
    DatabaseFeatures.connection_persists_old_columns = True
except ImproperlyConfigured:
    pass
