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

# a = owlready2.sync_reasoner()

class signatureSelector(object):

    def __init__(self, fileTypes, fileTriples):
        self.fileTypes = fileTypes
        self.fileTriples = fileTriples
        self.noTypeItems = set()
        self.Types = self.typeCreator()
        self.signedTypes = []
        self.noType = []

    def typeCreator(self):
        dictTypes = {}
        with open(self.fileTypes, 'r') as f:
            for line in f:
                typeAxiom = line.split(' ')
                typeAxiom[2] = typeAxiom[2].replace('<http://www.wikidata.org/entity/', '').replace(' .', '')
                typeAxiom[2] = typeAxiom[2].replace('>', '')
                if typeAxiom[0] in dictTypes.keys():
                    if type(dictTypes[typeAxiom[0]]) is not 'list':
                        typeList = []
                        typeList.append(dictTypes[typeAxiom[0]])
                        typeList.append(typeAxiom[2])
                    else:
                        dictTypes[typeAxiom[0]].append(typeAxiom[2])
                else:
                    dictTypes[typeAxiom[0].replace('<http://www.wikidata.org/entity/', '').replace('>', '')] = typeAxiom[2]

        return(dictTypes)


    def signatureCreator(self):
        tripleList = []
        tripleNoType = []
        signatureSet = set()
        with open(self.fileTriples, 'r') as t:
            for line in t:
                triple = line.split(' ')
                tripleSignature =self.tripleSignature([x.replace('<http://www.wikidata.org/entity/', '').replace('<http://www.wikidata.org/prop/direct/', '').replace('.\n', '').replace('>', '') for x in triple[:3]])
                if any(s is 'NA' for s in tripleSignature):
                    tripleNoType.append(tuple(triple[:3]))
                else:
                    if tripleSignature not in signatureSet:
                        signatureSet.add(tripleSignature)
                        tripleList.append(tuple(triple[:3]))

        # return(tripleList, tripleNoType)
        self.signedTypes = tripleList
        self.noType = tripleNoType


    def tripleSignature(self, triList):
        try:
            subjectType = self.Types[triList[0]]
        except KeyError:
            self.noTypeItems.add(triList[0])
            subjectType = 'NA'

        try:
            objectType = self.Types[triList[2]]
        except KeyError:
            self.noTypeItems.add(triList[2])
            objectType ='NA'

        tripleSig = (subjectType, triList[1], objectType)

        return(tripleSig)


    def fileWriterCharacteristicSigned(self):
        with open('WDSignedtriples.nt', 'w') as s:
            for triple in self.signedTypes:
                s.write(' '.join(triple) + ' .\n')
            s.close()

    def fileWriterNoType(self):
        with open('WDNoTypeTriples.nt', 'w') as s:
            for triple in self.noType:
                s.write(' '.join(triple) + ' .\n')
            s.close()

    def fileNoType(self):
        with open('WDMissingTypes.txt', 'w') as s:
            for i in self.noTypeItems:
                s.write(i +'\n')
            s.close()


def main():
    fileTypes = sys.argv[1]
    fileTriples = sys.argv[2]
    x = signatureSelector(fileTypes, fileTriples)
    x.signatureCreator()
    x.fileWriterCharacteristicSigned()
    x.fileWriterNoType()
    x.fileNoType()


if __name__ == "__main__":
    main()

