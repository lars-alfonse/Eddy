import pickle


def savePickle(object):
    pobject = pickle.dumps(object, pickle.HIGHEST_PROTOCOL)
    return pobject

def loadPickle(object):
    loadedObject = pickle.load(object)
    return loadedObject