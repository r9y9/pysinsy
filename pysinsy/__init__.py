import pkg_resources

from .sinsy import Sinsy
from .version import __version__  # noqa

DEFAULT_DIC_DIR = pkg_resources.resource_filename(__name__, "_dic")

DEFAULT_HTS_VOICE = pkg_resources.resource_filename(
    __name__, "htsvoice/nitech_jp_song070_f001.htsvoice"
)

# Global instance of sinsy
_global_sinsy = None


def get_default_dic_dir():
    """Returns default dictionary directory

    Returns:
        str: dictionary path
    """
    return DEFAULT_DIC_DIR


def get_default_htsvoice():
    """Returns default hts voice

    Returns:
        str: hts voice path
    """
    return DEFAULT_HTS_VOICE


def _lazy_init():
    global _global_sinsy
    _global_sinsy = Sinsy()
    _global_sinsy.setLanguages("j", get_default_dic_dir())
    _global_sinsy.loadVoices(get_default_htsvoice())


def synthesize(musicxml_path: str):
    """Synthesize waveform given muxic XML file

    Args:
        str: music XML path

    Returns:
        tuple: tuple of wav array of type float64 and sampling frequency

    Raises:
        RuntimeError: if fail to synthesize
    """
    global _global_sinsy
    if _global_sinsy is None:
        _lazy_init()

    _global_sinsy.loadScoreFromMusicXML(musicxml_path)
    wav, sr = _global_sinsy.synthesize()
    _global_sinsy.clearScore()

    return wav, sr
