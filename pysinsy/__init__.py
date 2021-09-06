import pkg_resources

from .sinsy import DEFAULT_DIC_DIR, Sinsy  # noqa
from .version import __version__  # noqa

DEFAULT_HTS_VOICE = pkg_resources.resource_filename(
    __name__, "htsvoice/nitech_jp_song070_f001.htsvoice"
)

# Global instance of sinsy
_global_sinsy = None


def get_default_dic_dir():
    return DEFAULT_DIC_DIR


def get_default_htsvoice():
    return DEFAULT_HTS_VOICE


def synthesize(musicxml_path: str):
    global _global_sinsy
    if _global_sinsy is None:
        _global_sinsy = Sinsy()
        _global_sinsy.setLanguages("j", get_default_dic_dir())
        _global_sinsy.loadVoices(get_default_htsvoice())

    _global_sinsy.loadScoreFromMusicXML(musicxml_path)
    wav, sr = _global_sinsy.synthesize()
    _global_sinsy.clearScore()

    return wav, sr
