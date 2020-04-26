# coding: utf-8

from .version import __version__

from .sinsy import Sinsy

_global_sinsy = None


def _lazy_init():
    pass
