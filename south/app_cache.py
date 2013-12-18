from django.db.models.loading import AppCache as DjangoAppCache, cache as app_cache
from django.utils.datastructures import SortedDict


class AppCache(DjangoAppCache):
    """
    A modification of AppCache into a version that can be instantiated
    multiple times.
    """

    def __init__(self):
        self.__dict__ = dict(
            app_store=SortedDict(),
            app_labels={},
            app_models=SortedDict(),
            app_errors={},
            loaded=False,
            handled=set(),
            postponed=[],
            nesting_level=0,
            _get_models_cache={},
            available_apps=None,
        )
        self.loaded = True
