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
                typeSubject = typeAxiom[0].replace('<http://www.wikidata.org/entity/', '').replace('>', '')
                if typeSubject in dictTypes.keys():
                    objectList = dictTypes[typeSubject]
                    if type(objectList) is not tuple:
                        typeList = (dictTypes[typeSubject],)
                        typeList = typeList + (typeAxiom[2], )
                        dictTypes[typeSubject] = typeList
                    else:
                        objectList = objectList + (typeAxiom[2], )
                        dictTypes[typeSubject] = objectList
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
            # print(subjectType)
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

    def getSignedTypes(self):
        counter = 0
        fileCounter = 0
        savedTypes = []
        savedTriples = []
        for statement in self.signedTypes:
            subjectT = statement[0].replace('<http://www.wikidata.org/entity/', '').replace('>', '')
            sType = self.Types[subjectT]
            if type(sType) is tuple:
                for item in sType:
                    statSubject = statement[0] + ' <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.wikidata.org/entity/' + item + '> .\n'
                    savedTypes.append(statSubject)
            else:
                statSubject = statement[0] + ' <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.wikidata.org/entity/' + sType + '> .\n'
                savedTypes.append(statSubject)

            objectT = statement[2].replace('<http://www.wikidata.org/entity/', '').replace('>', '')
            oType = self.Types[objectT]
            if type(oType) is tuple:
                for item in oType:
                    statObject = statement[2] + ' <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.wikidata.org/entity/' + item + '> .\n'
                    savedTypes.append(statObject)
            else:
                statObject = statement[2] + ' <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.wikidata.org/entity/' + oType + '> .\n'
                savedTypes.append(statObject)

            savedTriples.append(statement)
            counter += 1
            if counter == 25:
                fileCounter += 1
                self.fileWriterMini(fileCounter, savedTriples, savedTypes)
                savedTriples = []
                savedTypes = []
                counter = 0

            # print(statement, statSubject)

        # self.savedTypes = savedTypes

    def fileWriterMini(self, counter, savedTriples, savedTypes):
        fileName = 'WDSignedfiles-' +str(counter) +'.nt'

        with open(fileName, 'w') as s:
            for triple in savedTriples:
                s.write(' '.join(triple) + ' .\n')

            for i in savedTypes:
                s.write(i)
            s.close()

    def fileWriterCharacteristicSigned(self):
        with open('WDSignedtriples-triples.nt', 'w') as s:
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

    def fileTypesWrite(self):
        with open('WDSignedtriples-types.nt', 'w') as s:
            for i in self.savedTypes:
                s.write(i)
            s.close()


def main():
    fileTypes = sys.argv[1]
    fileTriples = sys.argv[2]
    x = signatureSelector(fileTypes, fileTriples)
    x.signatureCreator()
    # x.fileWriterCharacteristicSigned()
    x.getSignedTypes()
    # x.fileTypesWrite()
    # x.fileWriterNoType()
    # x.fileNoType()


if __name__ == "__main__":
    main()

