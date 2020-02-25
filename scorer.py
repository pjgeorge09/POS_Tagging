# -*- coding: utf-8 -*-
"""
Modified from ngram.py on 02/22/2020
   TODO: Parse that ambiguous definition thing. | 
"""
from sys import argv
import re
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
'''Handle command line arguments'''
MyFile = str(argv[1]) 
TrueFile = str(argv[2])

File = open(MyFile , 'r')
myTags = File.read()
myTags = re.sub('(.*)/', '', myTags)
myTags = re.split(r'\s+', myTags)
File2 = open(TrueFile, 'r')
trueTags = File2.read()
trueTags = re.sub('(.*)/', '', trueTags)
trueTags = re.split(r'\s+', trueTags)
File.close()

File2.close()

correct = 0
total = 0
for x in range(0 , len(trueTags)-1):
    if(myTags[x] == trueTags[x]):
        correct += 1
    total += 1

print("Number Correct : " + str(correct))
print("Number Total : " + str(total))
print("Percent : " + str(correct*100/total))





y_actu = pd.Series(trueTags, name='Actual')
y_pred = pd.Series(myTags, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
pd.set_option('display.expand_frame_repr', False)
print("Confusion matrix:\n%s" % df_confusion)


# for _ in myTags:
#     print(_)
