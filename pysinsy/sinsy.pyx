# cython: boundscheck=True, wraparound=True
# cython: c_string_type=unicode, c_string_encoding=ascii

import numpy as np

cimport numpy as np
np.import_array()

cimport cython
from libcpp.string cimport string
from libcpp.vector cimport vector

from .sinsy cimport sinsy, label_strings


cdef class LabelStrings(object):
    cdef label_strings.LabelStrings* ptr

    def getData(self):
        assert self.ptr is not NULL
        cdef char** data = <char**> self.ptr.getData()
        cdef size_t size = self.ptr.size()
        r = []
        cdef int i
        for i in range(size):
            r.append(<str>(data[i]))
        return r

    def __dealloc__(self):
        if self.ptr is not NULL:
            del self.ptr

cdef class SynthCondition(object):
    """Sinsy
    """
    cdef sinsy.SynthCondition* ptr
    cdef vector[double] buffer

    def __cinit__(self):
        self.ptr = new sinsy.SynthCondition()
        self.buffer = vector[double]()
        self._setWaveformBuffer(self.buffer)

    def setPlayFlag(self):
        self.ptr.setPlayFlag()

    def unsetPlayFlag(self):
        self.ptr.unsetPlayFlag()

    def setSaveFilePath(self, s):
        cdef string ss = s
        self.ptr.setSaveFilePath(ss)

    def unsetSaveFilePath(self):
        self.ptr.unsetSaveFilePath()

    cdef _setWaveformBuffer(self, vector[double]& x):
        self.ptr.setWaveformBuffer(x)

    def getWaveformBuffer(self):
        cdef np.ndarray waveform = np.zeros([self.buffer.size()], dtype=np.float64)
        waveform[:] = self.buffer[:]
        self.buffer.clear()
        return waveform

    def __dealloc__(self):
        del self.ptr


cdef class Sinsy(object):
    """Sinsy

    The core Sinsy class
    """
    cdef sinsy.Sinsy* ptr

    def __cinit__(self):
        self.ptr = new sinsy.Sinsy()

    def setLanguages(self, lang, config):
        """Set language

        Args:
            lang (str): language code.
            config (str): Path to dictionary.
        """
        return self.ptr.setLanguages(lang, config)

    def loadVoices(self, voice):
        """Load hts voice

        Args:
            voice (str): Path to hts voice.
        """
        cdef vector[string] voices
        voices.push_back(voice)
        cdef char ret
        ret = self.ptr.loadVoices(voices)
        return ret

    def setAlpha(self, alpha):
        """Set alpha

        Args:
            alpha (float): Alpha
        """
        return self.ptr.setAlpha(alpha)

    def setVolume(self, volume):
        """Set volume

        Args:
            volume (float): volume
        """
        return self.ptr.setVolume(volume)

    def createLabelData(self, monophoneFlag=False, overwriteEnableFlag=1, timeFlag=1):
        """Create labels

        Args:
            monophoneFlag (bool): Monophone or full-context
            overwriteEnableFlag (int): Overrite or not
            timeFlag (int): with time or not.

        Returns:
            LabelStrings: labels
        """
        cdef label_strings.LabelStrings* p
        p = self.ptr.createLabelData(monophoneFlag, overwriteEnableFlag, timeFlag)
        cdef LabelStrings label = LabelStrings()
        label.ptr = p
        return label

    def synthesize(self):
        """Synthesize waveform

        Returns:
            wav (ndarray): numpy array of type float64.
            sr (int): sampling frequency.

        Raises:
            RuntimeError: if fail to synthesize
        """
        cond = SynthCondition()
        cond.setPlayFlag()
        ret = self.ptr.synthesize(cond.ptr)
        if ret == False:
            raise RuntimeError("Failed to synthesize")
        wav = cond.getWaveformBuffer()
        sr = self.get_sampling_frequency()
        return wav, sr

    def clearScore(self):
        """Clear loaded score"""
        self.ptr.clearScore()

    def loadScoreFromMusicXML(self, xml):
        """Load score from music xml

        Args:
            xml (str): Path to music xml.
        """
        return self.ptr.loadScoreFromMusicXML(xml)

    def get_sampling_frequency(self):
        """Get sampling frequency

        Returns:
            int: sampling rate.
        """
        return self.ptr.get_sampling_frequency()

    def __dealloc__(self):
        del self.ptr
