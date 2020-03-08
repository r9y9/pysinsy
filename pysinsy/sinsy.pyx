# coding: utf-8
# cython: boundscheck=True, wraparound=True
# cython: c_string_type=unicode, c_string_encoding=ascii

import numpy as np

cimport numpy as np
np.import_array()

cimport cython


from sinsy cimport sinsy, label_strings

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


cdef class Sinsy(object):
    """Sinsy
    """
    cdef sinsy.Sinsy* ptr

    def __cinit__(self):
        self.ptr = new sinsy.Sinsy()

    def setLanguages(self, lang="j", config="/usr/local/lib/sinsy/dic"):
        return self.ptr.setLanguages(lang, config)

    def setAlpha(self, alpha):
        return self.ptr.setAlpha(alpha)

    def setVolume(self, alpha):
        return self.ptr.setVolume(alpha)

    def createLabelData(self):
        cdef label_strings.LabelStrings* p 
        p = self.ptr.createLabelData()
        cdef LabelStrings label = LabelStrings()
        label.ptr = p
        return label
    
    def clearScore(self):
        self.ptr.clearScore()
    
    def loadScoreFromMusicXML(self, xml):
        return self.ptr.loadScoreFromMusicXML(xml)
        
    def __dealloc__(self):
        del self.ptr
