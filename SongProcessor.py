import numpy
import SongData, WaveReader, NoteTranslator, DatabaseAccess

class SongProcessor():
    song = SongData.SongData()
    reader = WaveReader.WaveReader()
    translator = NoteTranslator.NoteTranslator()
    splitSignal = []

    def process(self, file, filename):
        self.song = self.reader.readWave(file, filename)
        self.splitSignal = numpy.array_split(self.song.signal, self.song.beats)
        for index in range(0, len(self.splitSignal)):
            if index >= len(self.splitSignal):
                continue
            note = self.translator.signalToNote(self.splitSignal[index], self.song.sampleRate)
            self.song.note_on_beat.append((note, index))
        self.patternDetector()
        cleanpattern = self.song.pattern.replace("#",'')
        self.song.pattern = cleanpattern
        DatabaseAccess.saveSong(self.song, file)

    def patternDetector(self):
        index = 1
        while index < len(self.song.note_on_beat):
            self.song.pattern += self.song.note_on_beat[index][0][0]
            index+=4
