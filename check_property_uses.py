#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

import ujson
import re
import bz2
import os
import sys
import pandas as pd
import urllib.parse
import csv

class fileHandler(object):

    def __init__(self, fileNT, fileTriples, fileOut):
        self.fileNT = fileNT
        self.fileTriples = fileTriples
        self.fileOut = fileOut
        self.defEntities = self.fileAnalyser()
        self.fileWriter(self.defEntities)

    def tripleExtractor(self):
        with open(self.fileTriples, 'r') as f:
            entityDict = {}
            for line in f:
                dictOrd = line.split(',')
                entityDict[dictOrd[0]] = dictOrd[1].replace('\n', '')

        return entityDict

    def fileAnalyser(self):
        # tripleCount = pd.read_csv(self.fileTriples, header=0)
        writingLine = []
        tripleCount = self.tripleExtractor()
        with open(self.fileNT, 'r') as f:
            for line in f:
                entity = line.split(' ')[0].replace('<', '').replace('>', '')
                if entity in tripleCount.keys():
                    if int(tripleCount[entity]) > 2:
                        writingLine.append(line)
        return writingLine

    def fileWriter(self, results):
        with open(self.fileOut, 'w') as f:
            for item in results:
                f.write("%s" % item)
        f.close()


def main():
    file_name = sys.argv[1]
    file_triples = sys.argv[2]
    file_output = sys.argv[3]
    fileHandler(file_name,file_triples, file_output)

if __name__ == "__main__":
    main()
