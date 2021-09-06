# distutils: language = c++

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector import vector

cdef extern from "LabelStrings.h" namespace "sinsy":
    cdef cppclass LabelStrings:
      void LabelStrings()
      size_t size()
      const char* const* getData()