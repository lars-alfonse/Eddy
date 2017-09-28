import librosa, collections, math

class SignalCreator():
    signal = []
    sampleRate = 0
    datasize = 0

    def setSampleRate(self, rate):
        self.sampleRate = rate

    def setDatasize(self, size):
        self.datasize = size

    def generateSignalFromNotes(self, notes):
        for note in notes:
            note = note[0] + '4'
            frequency = librosa.note_to_hz(note)
            data = [math.sin(2*math.pi*(x/self.sampleRate)) for x in range(self.datasize)]
            for sample in data:
                self.signal.append(sample)
        return self.signal
    