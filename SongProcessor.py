import numpy
import SongData, WaveReader, NoteTranslator, DatabaseAccess

def process(file, filename):
    reader = WaveReader.WaveReader()
    translator = NoteTranslator.NoteTranslator()
    song = reader.readWave(file, filename)
    splitSignal = numpy.array_split(song.signal, song.beats)
    for index in range(0, len(splitSignal)):
        if index >= len(splitSignal):
            continue
        note = translator.signalToNote(splitSignal[index], song.sampleRate)
        song.note_on_beat.append((note, index))
    song = patternDetector(song)
    cleanpattern = song.pattern.replace("#",'')
    song.pattern = cleanpattern
    DatabaseAccess.saveSong(song, file)

def patternDetector(song):
    index = 1
    while index < len(song.note_on_beat):
        song.pattern += song.note_on_beat[index][0][0]
        index+=4

    return song