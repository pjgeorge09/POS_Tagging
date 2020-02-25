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

'''Handle command line arguments'''
train = str(argv[1]) 

'''Preprocessing done here'''
File = open(train, 'r')
toAdd = File.read()
toAdd = removeBrackets(toAdd)
toAdd = re.sub('\|\S+', '', toAdd)
toAdd = re.split(r'\s+', toAdd)

for _ in toAdd:
    print(_)
    
    