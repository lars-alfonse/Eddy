import pickle


def savePickle(object):
    pobject = pickle.dumps(object)
    return pobject

def loadPickle(object):
    loadedObject = pickle.load(object)
    return loadedObject