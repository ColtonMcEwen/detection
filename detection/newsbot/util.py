from newsbot.models import *
import numpy as np

# Load up the canonical dictionary from the db
def loadCanonDict():
    canonDict = DictEntry.objects.all()
    dictSize = canonDict.count() + 1
    cDict = {}
    for cw in canonDict:
        cDict[cw.canonWord] = cw.pk

    return cDict

# Take in some text, spit out a row vector
def buildExampleRow(body_text, cDict):
    dictSize = len(cDict.keys())
    one_ex_vector = np.zeros(dictSize+2)
    cwords = body_text.split()
    for word in cwords:
        if(word in cDict.keys()):
            one_ex_vector[cDict[word]-1] = 1
        else:
            print("This word doesn't exist in the dict:" + word)

    return(one_ex_vector)

# Using examples from the db, process them into a training set
def processExamples(qs_Examples, cDict):
    Y_vector = np.zeros(qs_Examples.count(), dtype=np.int8)
    Y_vec_count = 0
    examplesMatrix = None

    for ex in qs_Examples:
        Y_vector[Y_vec_count] = int(ex.quality_class)
        Y_vec_count = Y_vec_count + 1
        if(examplesMatrix is None):
            examplesMatrix = buildExampleRow(ex.body_text, cDict)
        else:
            examplesMatrix = np.vstack([examplesMatrix, buildExampleRow(ex.body_text, cDict)])
        print('.', end='', flush=True)

    return( (Y_vector, examplesMatrix))


