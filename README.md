# Pysinsy

A python wrapper for https://github.com/r9y9/sinsy.

Please notice that the package is not ready to use and APIs will subject to change.

I will tag a release once I finish the initial design.

I'm focusing on porting the frontend functionality (i.e., extracting full context labels from a musicxml file), but feel free to ask me if you have any request.

## Quick demo

```py
import pysinsy


s = pysinsy.sinsy.Sinsy()
assert s.setLanguages("j", "/usr/local/lib/sinsy/dic")
assert s.loadScoreFromMusicXML("./sample1.musicxml")
label = s.createLabelData()
for l in label.getData():
    print(l)
```
```
$ python a.py | cat | head -2
0 24000000 p@xx^xx-pau+h=a_xx%xx^00_00~00-1!1[xx$xx]xx/A:xx-xx-xx@xx~xx/B:1_1_1@xx|xx/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:xx]xx^0=4/4~100!1@240#96+xx]1$1|0[24&0]96=0^100~xx#xx_xx;xx$xx&xx%xx[xx|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+xx!xx^xx/F:G4#7#0-4/4$100$1+60%24;xx/G:xx_xx/H:xx_xx/I:10_10/J:3~3@8
24000000 -1 c@xx^pau-h+a=r_xx%00^00_00~00-1!2[xx$1]xx/A:xx-xx-xx@xx~xx/B:2_1_1@JPN|0/C:2+1+1@JPN&0/D:xx!xx#xx$xx%xx|xx&xx;xx-xx/E:G4]7^0=4/4~100!1@60#24+xx]1$5|0[24&0]96=0^100~1#10_0;47$0&192%0[100|0]0-n^xx+xx~xx=xx@xx$xx!xx%xx#xx|xx|xx-xx&xx&xx+xx[xx;xx]xx;xx~xx~xx^xx^xx@xx[xx#xx=xx!xx~xx+m3!xx^xx/F:E4#4#0-4/4$100$1+30%12;xx/G:xx_xx/H:10_10/I:5_5/J:3~3@8
```