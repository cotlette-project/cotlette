import os
import functools
from collections import Counter
from pathlib import Path

from cotlette.apps import apps
from cotlette.conf import settings
from cotlette.core.exceptions import ImproperlyConfigured
from cotlette.utils.functional import cached_property
from cotlette.utils.module_loading import import_string


class InvalidTemplateEngineError(ImproperlyConfigured):
    pass


class EngineHandler:
    def __init__(self, templates=None):
        """
        templates is an optional list of template engine definitions
        (structured like settings.TEMPLATES).
        """
        self._templates = templates
        self._engines = {}

    @cached_property
    def templates(self):
        if self._templates is None:
            self._templates = settings.TEMPLATES

        templates = {}
        backend_names = []
        for tpl in self._templates:
            try:
                # This will raise an exception if 'BACKEND' doesn't exist or
                # isn't a string containing at least one dot.
                default_name = tpl["BACKEND"].rsplit(".", 2)[-2]
            except Exception:
                invalid_backend = tpl.get("BACKEND", "<not defined>")
                raise ImproperlyConfigured(
                    "Invalid BACKEND for a template engine: {}. Check "
                    "your TEMPLATES setting.".format(invalid_backend)
                )

            tpl = {
                "NAME": default_name,
                "DIRS": [],
                "APP_DIRS": False,
                "OPTIONS": {},
                **tpl,
            }

            templates[tpl["NAME"]] = tpl
            backend_names.append(tpl["NAME"])

        counts = Counter(backend_names)
        duplicates = [alias for alias, count in counts.most_common() if count > 1]
        if duplicates:
            raise ImproperlyConfigured(
                "Template engine aliases aren't unique, duplicates: {}. "
                "Set a unique NAME for each engine in settings.TEMPLATES.".format(
                    ", ".join(duplicates)
                )
            )

        return templates

    def __getitem__(self, alias):
        try:
            return self._engines[alias]
        except KeyError:
            try:
                params = self.templates[alias]
            except KeyError:
                raise InvalidTemplateEngineError(
                    "Could not find config for '{}' "
                    "in settings.TEMPLATES".format(alias)
                )

            # If importing or initializing the backend raises an exception,
            # self._engines[alias] isn't set and this code may get executed
            # again, so we must preserve the original params. See #24265.

            params = params.copy()
            backend = params.pop("BACKEND")
            engine_cls = import_string(backend)
            engine = engine_cls(params)

            self._engines[alias] = engine

            return engine

    def __iter__(self):
        return iter(self.templates)

    def all(self):
        return [self[alias] for alias in self]


@functools.lru_cache
def get_app_template_dirs(dirname):
    """
    Return an iterable of paths of directories to load app templates from.

    dirname is the name of the subdirectory containing templates inside
    installed applications.
    """
    # Immutable return value because it will be cached and shared by callers.

    template_dirs = tuple()
    for app_config in apps.get_app_configs():
        if app_config.path:
            dir_name = os.path.join(app_config.path, dirname)
            if os.path.isdir(dir_name):
                template_dirs = template_dirs + (dir_name,)
    return template_dirs