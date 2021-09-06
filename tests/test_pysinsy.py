# coding: utf-8

from os.path import dirname, join

import pysinsy

DATA_DIR = dirname(__file__)


def test_pysinsy_frontend():
    # http://sinsy.sp.nitech.ac.jp/sample/song070_f00001_063.xml

    xml_path = join(DATA_DIR, "song070_f00001_063.xml")

    sinsy = pysinsy.sinsy.Sinsy()
    assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
    assert sinsy.loadScoreFromMusicXML(xml_path)

    for is_mono in [True, False]:
        label = sinsy.createLabelData(is_mono, 1, 1)
        for line in label.getData():
            print(line)

    sinsy.clearScore()


def test_pysinsy_synthesize():
    xml_path = join(DATA_DIR, "song070_f00001_063.xml")

    sinsy = pysinsy.sinsy.Sinsy()
    assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
    assert sinsy.loadScoreFromMusicXML(xml_path)
    assert sinsy.loadVoices(pysinsy.get_default_htsvoice())

    wav, sr = sinsy.synthesize()
    assert len(wav) > 0 and wav.max() > 0
    assert sr == 48000

    sinsy.clearScore()


def test_pysinsy_highlevel():
    xml_path = join(DATA_DIR, "song070_f00001_063.xml")

    for _ in range(3):
        wav, sr = pysinsy.synthesize(xml_path)
        assert len(wav) > 0 and wav.max() > 0
        assert sr == 48000
