"""
Copyright (C) 2020-2021 Jiri Borovec <...>
"""
import os

__version__ = "0.3.2"
__docs__ = "Deprecation tooling"
__author__ = "Jiri Borovec"
__author_email__ = "jiri.borovec@fel.cvut.cz"
__homepage__ = "https://borda.github.io/pyDeprecate"
__source_code__ = "https://github.com/Borda/pyDeprecate"
__license__ = 'MIT'

_PATH_PACKAGE = os.path.realpath(os.path.dirname(__file__))
_PATH_PROJECT = os.path.dirname(_PATH_PACKAGE)

from deprecate.deprecation import deprecated  # noqa: F401 E402
from deprecate.utils import void  # noqa: F401 E402
