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
    classLines = []
    with open(fileName, 'r') as f:
        for line in f:
            if '<rdf:Description rdf:about=' in line:
                about = line[17:-2]
                newLine = '<owl:Class ' + about + '/>'
                classLines.append(newLine)

    # print(len(matchingClasses))
    return classLines


def writeMappings(mappings, fileName):
    ###write properties
    with open(fileName, 'a') as f:
        mappingLines = '\n'.join(mappings)
        f.write(mappingLines)
        f.close()



def main():
    file_name = sys.argv[1]
    # class_file = sys.argv[2]

    x = yagoAligner(file_name)
    writeMappings(x, file_name)

if __name__ == "__main__":
    main()