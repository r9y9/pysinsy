# distutils: language = c++

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

from .label_strings cimport LabelStrings

cdef extern from "sinsy.h" namespace "sinsy":
   cdef cppclass SynthCondition:
      SynthCondition()
      void setPlayFlag()
      void unsetPlayFlag()
      void setSaveFilePath(const string& filePath)
      void unsetSaveFilePath()
      void setWaveformBuffer(vector[double]& waveform)
      void unsetWaveformBuffer()


   cdef cppclass Sinsy:
      Sinsy()
      bool setLanguages(const string& languages, const string& configs)
      bool loadVoices(const vector[string]& voices)

      bool setAlpha(double alpha)
      bool setVolume(double volume)

      LabelStrings* createLabelData(bool monophoneFlag, int overwriteEnableFlag, int timeFlag)

      bool synthesize(SynthCondition* condition)
      bool stop()
      bool resetStopFlag()
      bool clearScore()

      bool loadScoreFromMusicXML(const string& xml)

      size_t get_sampling_frequency()