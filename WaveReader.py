import librosa
import SongData

class WaveReader():

    def readWave(self, file, filename):
        song = SongData.SongData()
        song.name = filename

        song.signal, song.sampleRate = librosa.load(file)
        song.tempo = round(librosa.beat.tempo(song.signal)[0])
        song.beats = ((len(song.signal)/song.sampleRate)/60)*song.tempo
        song.seconds = song.beats*(60/song.tempo)
        return song

