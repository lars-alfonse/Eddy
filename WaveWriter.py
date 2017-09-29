import wave, struct


class WaveWriter(object):
    datasize = 0
    filename = ""
    readwrite = "w"
    channelcount = 1
    samplewidth = 2
    samplerate = 0
    framecount = 0
    comptype = "NONE"
    compname = "not compressed"

    def setParams(self, channel, width, rate, frame, type, name):
        if channel != "default":
            self.channelcount = channel
        if width != "default":
            self.samplewidth = width
        if type != "default":
            self.comptype = type

        self.samplerate = rate
        self.framecount = frame


    def setFileName(self, path):
        self.filename = path

    def writeWave(self, data):
        file = wave.open(self.filename, self.readwrite)
        file.setparams(self.channelcount, self.samplewidth, self.samplerate, self.framecount, self.comptype, self.compname)
        for sample in data:
            file.writeframes(struct.pack('h', int(sample*64000/2)))
        file.close()
