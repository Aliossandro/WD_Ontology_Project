#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson
import bz2
import sys

def writeClasslist(classList, file_name):
    ###write properties
    with open(file_name, 'w') as f:
        f.write(classList)
        f.close()


def classExtractor(file_name):
    classesList = []
    classesP31 = []

    # open dumps
    with bz2.BZ2File(file_name, 'r') as f:

        for line in f:

            try:
                lineParsed = ujson.loads(line[:-2])

                if 'P279' in lineParsed['claims'].keys():
                    entityID = lineParsed['id']
                    classesList.append(entityID)
                    for i in lineParsed['claims']['P279']:
                        try:
                            superClass = i['mainsnak']['datavalue']['value']['id']
                            classesList.append(superClass)
                        except:
                            print(i)

                elif 'P31' in lineParsed['claims'].keys():
                    for i in lineParsed['claims']['P31']:
                        try:
                            superClass = i['mainsnak']['datavalue']['value']['id']
                            classesP31.append(superClass)
                        except:
                            print(i)

        return classesList, classesP31


def main():
    file_name = sys.argv[1]
    classesAll = classExtractor(file_name)
    classP279 = set(classesAll[0])
    classP31 = set(classesAll[1])

    #write files
    writeClasslist(classP279, 'classesP279.txt')
    writeClasslist(classP31, 'classesP31.txt')


if __name__ == "__main__":
    main()