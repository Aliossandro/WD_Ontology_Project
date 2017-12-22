#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

# import ujson
import re
# import bz2
import os
import sys
# import pandas as pd
# import urllib.parse
# import csv
# import owlready2

with open(fileName, 'r') as f:
    save = False
    propertyList = []

    for line in f:

        if save and line.startswith('</owl:ObjectProperty'):
            propertyList.append(line)
            save = False

        if save and not line.startswith('<wdt:'):
            if not line.startswith('<rdf:type rdf:resource="http://www.wikidata.org/entity/') or not line.startswith('<rdf:type rdf:resource="http://wikiba.se/ontology-beta'):
                propertyList.append(line)

        if save is False and line.startswith('<owl:ObjectProperty'):
            save = True
            if line not in propertyList:
                propertyList.append(line)


fileName = '/Users/alessandro/Documents/PhD/WDOntology_100k_modified.owl'
fileName2 = '/Users/alessandro/Documents/PhD/Classesonly2.xml'
fileClasses = '/Users/alessandro/Documents/PhD/WDClasses.owl'
fileNolabel = '/Users/alessandro/Documents/PhD/nolabelClasses.owl'
fileUndefined = '/Users/alessandro/Documents/PhD/undefinedClasses.xml'

with open(fileClasses, 'r') as b:
    classesList = []
    for linb in b:
        if '<owl:Class' in linb:
            classa = linb.strip().replace('/>', '>')
            classesList.append(classa)

with open(fileNolabel, 'r') as b:
    classesNolabel = []
    for linb in b:
        if '<owl:Class' in linb:
            classa = linb.strip().replace('/>', '>')
            classesNolabel.append(classa)

with open(fileUndefined, 'r') as b:
    classesUndefined = []
    for linb in b:
        if '<owl:Class' in linb:
            classa = linb.strip().replace('/>', '>')
            classesUndefined.append(classa)


classesNolabel = classesNolabel + classesUndefined
classesList = [x for x in classesList if x not in classesNolabel]

with open(fileName2, 'r') as f:
    save = True
    union = False
    somevalue = True
    propertyList = []


    for line in f:

        if line.startswith('<owl:unionOf') or line.startswith('<owl:DisjointUnion'):
            union = True

        if line.startswith('</owl:DisjointUnion') or line.startswith('</owl:unionOf>'):
            union = False

        if re.match(r'^</wdt:[Pp][0-9]{1,}>', line):
            print(line)
            save = True
            continue


        if line.startswith('<owl:Class rdf:about="http://www.wikidata.org/entity/'):
            if line.replace('\n', '') not in classesList:
                if union:
                    save =True
                else:
                    save = False
            else:
                save = True

        if save :
            if not line.startswith('<wdt:') and not line.startswith('<dcterms:'):
                propertyList.append(line)
            elif re.match('<wdt:[Pp][0-9]{1,}>', line):
                save = False







        # if save and line.startswith('</owl:Class'):
        #     propertyList.append(line)
        #     save = False
        #
        # if save and not line.startswith('<wdt:'):
        #     # if not line.startswith('<rdf:type rdf:resource="http://www.wikidata.org/entity/') or not line.startswith('<rdf:type rdf:resource="http://wikiba.se/ontology-beta'):
        #     propertyList.append(line)
        #
        # if save is False and line.startswith('<owl:Class rdf:about="http://www.wikidata.org/entity/'):
        #     save = True
        #     if (line in classesList) and (line not in propertyList):
        #         propertyList.append(line)



with open('WDObjectProperties.owl', 'w') as f:
    for i in propertyList:
        f.write(i)
    f.close()

with open('WDClasses_clean.owl', 'w') as f:
    for i in propertyList:
        f.write(i)
    f.close()

