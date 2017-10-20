#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

import ujson
import re
import bz2
import os
import fileWriter
from lxml import etree

def selector(filename, classList):
    allClasses = []
    WDclasses = classOpener(classList)
    with open(filename, 'r') as f:
        classLines = []
        for line in f:
            if any(WDclass in line for WDclass in WDclasses):
                print('yeah')
                print(line)
                classLines.append(line)
                for line in f:
                    if '</owl:Class>' in line:
                        classLines.append(line)
                        allClasses += classLines
                        classLines =[]
                        break
                    else:
                        classLines.append(line)
    return allClasses




def selectorTop(filename):
    allClasses = []
    # WDclasses = classOpener(classList)
    with open(filename, 'r') as f:
        classLines = []
        for line in f:
            if '<owl:Class rdf:about=' in line:
                # if any(WDclass in line for WDclass in WDclasses):
                #     print('yeah')
                #     print(line)
                classLines.append(line)
                for line in f:
                    if '<rdfs:subClassOf rdf:resource=' in line:
                        classLines = []
                        break
                    elif '</owl:Class>' in line:
                        classLines.append(line)
                        allClasses += classLines
                        classLines =[]
                        break
                    else:
                        classLines.append(line)
    return allClasses


def classOpener(filename):
    classesWD = []
    with open(filename, 'r') as f:
        for line in f:
            line = '<owl:Class rdf:about="http://www.wikidata.org/entity/' + line.replace('\n','') + '">'
            classesWD.append(line)
    return classesWD