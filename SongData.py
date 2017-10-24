class SongData(object):
    name = ""
    signal = []
    sampleRate = 0
    seconds = 0.0
    tempo = 0.0
    beats = 0.0
    note_on_beat = [()]
    path = ""
    pattern = ""
    def __init__(self):
        self.name = ""
        self.signal = []
        self.sampleRate = 0
        self.seconds = 0.0
        self.tempo = 0.0
        self.beats = 0.0
        self.note_on_beat = [()]
        self.path = ""
        self.pattern = ""