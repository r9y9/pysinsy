# Pysinsy

[![PyPI](https://img.shields.io/pypi/v/pysinsy.svg)](https://pypi.python.org/pypi/pysinsy)
![Python package](https://github.com/r9y9/pysinsy/workflows/Python%20package/badge.svg)
[![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md)
[![][docs-latest-img]][docs-latest-url]


[docs-latest-img]: https://img.shields.io/badge/docs-latest-blue.svg
[docs-latest-url]: https://r9y9.github.io/pysinsy/


A python wrapper for https://github.com/r9y9/sinsy.

Please notice that the package is in an alpha state. APIs will subject to change.

## Notice

The package is built with the [modified version of sinsy](https://github.com/r9y9/sinsy). The modified version provides the same functionality with some improvements (e.g., cmake support) but is technically different from the one from HTS working group.

## Build requirements

The python package relies on cython to make python bindings for sinsy. You must need the following tools to build and install pysinsy:

- C/C++ compilers (to build C/C++ extentions)
- cython

## Supported platforms

- Linux
- Mac OSX
- Windows (MSVC)

## Installation

```
pip install pysinsy
```

## Development

To build the package locally, you will need to make sure to clone sinsy.

```
git submodule update --recursive --init
```

and then run

```
pip install -e .
```

## Quick demo

```py
import pysinsy

sinsy = pysinsy.Sinsy()

# Set language to Japanese
assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
assert sinsy.loadScoreFromMusicXML("./tests/song070_f00001_063.xml")

print("Mono labels:")
is_mono = True
labels = sinsy.createLabelData(is_mono, 1, 1).getData()
for l in labels[:5]:
    print(l)

print("\nFull-context labels:")
is_mono = False
labels = sinsy.createLabelData(is_mono, 1, 1).getData()
for l in labels[:5]:
    print(l)

sinsy.clearScore()
```

Output:

```
Mono labels:
0 10909090 sil
10909090 21818181 sil
21818181 32727272 sil
32727272 43636363 pau
43636363 47727272 g

Full-context labels:
0 10909090 s@xx^xx-sil+sil=sil_xx%xx^00_00~00-1!1[xx$xx]xx/A:xx-xx-xx@xx~xx/B:1_1_1@xx|xx/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:xx]xx^0=2/4~110!1@109#48+xx]1$1|0[10&0]48=0^100~xx#xx_xx;xx$xx&xx%xx[xx|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+xx!xx^xx/F:A4#9#0-2/4$110$1+40%18;xx/G:xx_xx/H:xx_xx/I:12_12/J:2~2@3
10909090 21818181 s@xx^sil-sil+sil=pau_xx%00^00_00~00-1!1[xx$xx]xx/A:xx-xx-xx@xx~xx/B:1_1_1@xx|xx/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:xx]xx^0=2/4~110!1@109#48+xx]1$1|0[10&0]48=0^100~xx#xx_xx;xx$xx&xx%xx[xx|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+xx!xx^xx/F:A4#9#0-2/4$110$1+40%18;xx/G:xx_xx/H:xx_xx/I:12_12/J:2~2@3
21818181 32727272 s@sil^sil-sil+pau=g_00%00^00_00~00-1!1[xx$xx]xx/A:xx-xx-xx@xx~xx/B:1_1_1@xx|xx/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:xx]xx^0=2/4~110!1@109#48+xx]1$1|0[10&0]48=0^100~xx#xx_xx;xx$xx&xx%xx[xx|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+xx!xx^xx/F:A4#9#0-2/4$110$1+40%18;xx/G:xx_xx/H:xx_xx/I:12_12/J:2~2@3
32727272 43636363 p@sil^sil-pau+g=e_00%00^00_00~00-1!1[xx$xx]xx/A:xx-xx-xx@xx~xx/B:1_1_1@xx|xx/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:xx]xx^0=2/4~110!1@109#48+xx]1$1|0[10&0]48=0^100~xx#xx_xx;xx$xx&xx%xx[xx|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+xx!xx^xx/F:A4#9#0-2/4$110$1+40%18;xx/G:xx_xx/H:xx_xx/I:12_12/J:2~2@3
43636363 47727272 c@sil^pau-g+e=N_00%00^00_00~00-1!2[xx$1]xx/A:xx-xx-xx@xx~xx/B:2_1_1@JPN|0/C:1+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:A4]9^0=2/4~110!1@40#18+xx]1$4|0[10&0]48=0^100~1#12_0;38$0&168%0[100|0]0-n^xx+xx~xx=xx@xx$xx!2%xx#5|xx|24-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+p0!xx^xx/F:A4#9#0-2/4$110$1+13%6;xx/G:xx_xx/H:12_12/I:11_11/J:2~2@3
```
