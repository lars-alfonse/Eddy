import pickle


def savePickle(object):
    pobject = pickle.dumps(object, pickle.HIGHEST_PROTOCOL)
    return pobject

def loadPickle(object):
    file = open("file.obj", "wb")
    file.write(object)
    file.close()
    readfile = open("file.obj", "rb")
    loadedObject = pickle.load(readfile)
    readfile.close()
    return loadedObject