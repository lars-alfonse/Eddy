import librosa
import SongData

class WaveReader():

    def readWave(self, file):
        song = SongData.SongData()
        song.name = file.filename
        song.signal, song.sampleRate = librosa.load(file)
        song.tempo = round(librosa.beat.tempo(song.signal)[0])
        song.beats = ((len(song.signal)/song.sampleRate)/60)*song.tempo
        return song

