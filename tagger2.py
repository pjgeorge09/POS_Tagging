# -*- coding: utf-8 -*-
"""
Modified from ngram.py on 02/22/2020
   TODO: Parse that ambiguous definition thing. | 
"""
from sys import argv
import re
import numpy as np

''' Method to remove "[" and "]" '''
def removeBrackets(document):
    document = re.sub(r'\[ ', '', document)
    document = re.sub(r' \]', '', document)
    return document

'''-------------------------------------------------------------------------'''
'''---------------------------------MAIN------------------------------------'''
'''-------------------------------------------------------------------------'''

'''Handle command line arguments'''
train = str(argv[1]) 
test = str(argv[2])

'''Preprocessing done here'''
File = open(train, 'r')
toAdd = File.read()
# toAdd = "<>/<>\n" + toAdd
toAdd = removeBrackets(toAdd)
# toAdd = re.sub(r'\n|\\ufeff', ' ', toAdd) # Destroy these weird tokens
toAdd = re.sub('/\.', '/. <e>/<e> <s>/<s>', toAdd)  # Leave as toAdd = re.sub('/\.', '/. <>/<>', toAdd)
toAdd = re.sub('\|\S+', '', toAdd)
toAdd = re.split(r'\s+', toAdd)


wordFrequency = dict()
tagFrequency = dict()
tagGivenWord = dict() # Key 1 = Word , Key 2 = Tag , item = count
tagGivenPreviousTag = dict() # Key 1 = PTag , Key 2 = tag , item = count
previousWord = "<s>"
previousTag = "<s>"
thisWord = "" # Pierre
thisTag = "" # NNP
for _ in toAdd:
    temp = re.split('/',_)
    if(len(temp) < 2):
        continue
        
    thisWord = temp[0]
    thisTag = temp[1]
    # Add words to word frequencies
    if thisWord not in wordFrequency.keys():
        wordFrequency[thisWord] = 1
    else:
        wordFrequency[thisWord] += 1
    # Add tags to tag frequencies
    if thisTag not in tagFrequency.keys():
        tagFrequency[thisTag] = 1
    else:
        tagFrequency[thisTag] += 1

    # Case, word has never been seen before
    if thisWord not in tagGivenWord.keys():
        tagGivenWord[thisWord] = {}
        tagGivenWord[thisWord][thisTag] = 1
    # Case word has been seen 
    else:
        # BUT never seen with this tag
        if thisTag not in tagGivenWord[thisWord].keys():
            tagGivenWord[thisWord][thisTag] = 1
        # AND seen with this tag before
        else:
            tagGivenWord[thisWord][thisTag] += 1
    # Case, last tag has never been seen before     tagGivenPreviousTag[previousTag][thisTag] = integer
    if previousTag not in tagGivenPreviousTag.keys():
        tagGivenPreviousTag[previousTag] = {}
        tagGivenPreviousTag[previousTag][thisTag] = 1
    # Case, last tag has been seen 
    else:
        # BUT never seen with this tag
        if thisTag not in tagGivenPreviousTag[previousTag].keys():
            tagGivenPreviousTag[previousTag][thisTag] = 1
        # AND seen with this tag before
        else:
            tagGivenPreviousTag[previousTag][thisTag] += 1
    previousTag = thisTag
    previousWord = thisWord

''' Assigning values to the testing set '''
''' So you have a word. You want to know what it's part of speech is. We have a dictionary of the probabilities
    of words and their most likely parts of speech. We also have a dictionary of most likely parts of speech given
    the next part of speech.
    But what if we don't yet know what the next part of speech is...?
    So Word (A) could be of type (NN | NNP | NTS) and Word (B) could be of type (IN | NN | XX)
    So we do (Proability of (A | NN) * Probability of (NN | <>) * Probability of (B | IN) * Probability of (IN | NN)'''
File.close()

# print("FUCKSHIT")
''' Test Preprocessing done here'''
File2 = open(test, 'r')
toAdd2 = File2.read()
# toAdd2 = "<s>\n" + toAdd2
toAdd2 = removeBrackets(toAdd2)
## THIS IS THE PROBLEM. WORKS FINE WHEN COMMENTED OUT
# toAdd2 = re.sub(r'\s\.\n', ' . <e> <s> ', toAdd2)  # Leave as toAdd = re.sub('/\.', '/. <>/<>', toAdd)
toAdd2 = re.split(r'\s+', toAdd2)
tempDict = []

for _ in toAdd2:
    if _ == "." or _ == "?" or _ == "!":
        tempDict.append(str(_) + "\n<e>\n<s>")
    else:
        tempDict.append(str(_))
    # We know last is <>

# for _ in tempDict:
#     print(_)

def probability(tag, word, prevTag):
    global tagGivenPreviousTag
    global tagGivenWord
    return ((tagGivenWord[word][tag])/(wordFrequency[word]))*((tagGivenPreviousTag[prevTag][tag])/(tagFrequency[prevTag]))



# print("FUCKSHIT")
lastTag = "<s>"
output = []
''' Test Postprocessing '''
# For every word in train.txt
for currentWord in toAdd2:
    # print(currentWord)
    if(currentWord.isspace()):
        continue
    best = 0
    tagToAssign = ""
    if(currentWord in tagGivenWord.keys()):
        # For every tag that THIS WORD has,
        for aTag in tagGivenWord[currentWord].keys():
            # print(aTag)
            if aTag not in tagGivenPreviousTag[lastTag].keys():
                x = 0
            p1 = tagGivenWord[currentWord][aTag]
            p2 = wordFrequency[currentWord]
            if (aTag not in tagGivenPreviousTag[lastTag].keys()):
                tagGivenPreviousTag[lastTag][aTag] = 1
            p3 = tagGivenPreviousTag[lastTag][aTag]
            p4 = tagFrequency[lastTag]
            if ( (p1/p2)*(p3/p4)> best):
                best = ((tagGivenWord[currentWord][aTag])/(wordFrequency[currentWord]))*((tagGivenPreviousTag[lastTag][aTag])/(tagFrequency[lastTag]))
                tagToAssign = aTag
                # print("Did something)")
        # print(tagToAssign+ " TAG TO ASSIGN")
        lastTag = tagToAssign
        output.append(currentWord + "/" + tagToAssign)
    else:
        output.append(currentWord+"/NN")
# print("FUCKSHIT")
for _ in output:
    print(_)


    
    
        












    