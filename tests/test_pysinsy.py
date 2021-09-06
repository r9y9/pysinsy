# coding: utf-8

from os.path import dirname, join

import pysinsy

DATA_DIR = dirname(__file__)


def test_pysinsy():
    # http://sinsy.sp.nitech.ac.jp/sample/song070_f00001_063.xml

    xml_path = join(DATA_DIR, "song070_f00001_063.xml")

    sinsy = pysinsy.sinsy.Sinsy()
    assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
    assert sinsy.loadScoreFromMusicXML(xml_path)

    is_mono = True
    for is_mono in [True, False]:
        label = sinsy.createLabelData(is_mono, 1, 1)
        for l in label.getData():
            print(l)

    sinsy.clearScore()
