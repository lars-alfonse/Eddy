import numpy, librosa

class NoteTranslator():

    def signalToNote(self, signal, sampleRate):
        fftsignal = numpy.fft.fft(signal)
        freqcollection = numpy.fft.fftfreq(len(fftsignal))
        index = numpy.argmax(numpy.abs(fftsignal))
        freq = freqcollection[index]
        freq_in_hz = abs(freq * sampleRate)
        if freq_in_hz != 0.0:
            note = librosa.core.hz_to_note(freq_in_hz, octave = False)
            return note
        else:
            note = ['X']
            return note


