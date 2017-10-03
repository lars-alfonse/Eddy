import numpy
import SongData, WaveReader, NoteTranslator

class SongProcessor():
    song = SongData.SongData()
    reader = WaveReader.WaveReader()
    translator = NoteTranslator.NoteTranslator()
    splitSignal = []

    def process(self, file):
        self.song = self.reader.readWave(file)
        self.splitSignal = numpy.array_split(self.song.signal, self.song.beats)
        for index in range(0, self.song.beats):
            if index >= len(self.splitSignal):
                continue
            note = self.translator.signalToNote(self.splitSignal[index], self.song.sampleRate)
            self.song.note_on_beat.append((note, index))
