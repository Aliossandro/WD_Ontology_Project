#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

import ujson
import re
import bz2
import os
import fileWriter
import sys
import urllib.parse

def yagoAligner(fileName):
    # classesList = fileWriter.classesReader(classFile)
    matchingClasses = []
    with open(fileName, 'r') as f:
        for line in f:
            try:
                line = line.split('\t')
                lineMatched = re.search(r'[qQ][0-9]{1,}', line[2])
                itemId = lineMatched.group(0)
                # if itemId in classesList:
                yagoId = line[0].replace('<', '<http://yago-knowledge.org/resource/')
                yagoId = urllib.parse.quote_plus(yagoId, safe='><-=+://')
                wdItem = line[2].replace(" .", "").replace('\n', '')
                lineToWrite = wdItem + "\t" + line[1] + "\t" + yagoId + ' .'
                matchingClasses.append(lineToWrite)

            except IndexError as e:
                print(e)
                print(line)
            except AttributeError as a:
                print(a)
                print(line)

    # print(len(matchingClasses))
    return matchingClasses


def writeMappings(mappings):
    ###write properties
    with open('wd-yago.ttl', 'w') as f:
        x = fileWriter.OntologyFile(f, 'ttl')
        x.secondWriter(mappings)



def main():
    file_name = sys.argv[1]
    # class_file = sys.argv[2]

    x = yagoAligner(file_name)
    writeMappings(x)

if __name__ == "__main__":
    main()