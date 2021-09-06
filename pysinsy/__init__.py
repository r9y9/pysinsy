import pkg_resources

from .sinsy import Sinsy  # noqa
from .version import __version__

_DEFAULT_DIC_DIR = pkg_resources.resource_filename(__name__, "_dic")

__all__ = ["Sinsy", "get_default_dic_dir", "__version__"]


def get_default_dic_dir():
    return _DEFAULT_DIC_DIR
