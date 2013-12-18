from functools import wraps
from south.patches import add_to_module
from django.db import DEFAULT_DB_ALIAS, connections
from django.utils.decorators import available_attrs


@add_to_module("django.db.transaction")
class Atomic(object):
    """
    This class is a mere shadow of the real Atomic class that attempts
    to map the behaviour to old transactions enough that migrations can run.
    """

    def __init__(self, using, savepoint):
        self.using = using
        self.savepoint = savepoint

    def __enter__(self):
        connection = connections[self.using]
        connection.enter_transaction_management()

    def __exit__(self, exc_type, exc_value, traceback):
        connection = connections[self.using]
        if exc_type is None:
            connection.commit()
        else:
            connection.rollback()
        connection.leave_transaction_management()

    def __call__(self, func):
        @wraps(func, assigned=available_attrs(func))
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner


@add_to_module("django.db.transaction")
def atomic(using=None, savepoint=True):
    # Bare decorator: @atomic -- although the first argument is called
    # `using`, it's actually the function being decorated.
    if callable(using):
        return Atomic(DEFAULT_DB_ALIAS, savepoint)(using)
    # Decorator: @atomic(...) or context manager: with atomic(...): ...
    else:
        return Atomic(using, savepoint)
