#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson
import bz2
import sys

def writeClasslist(classList, file_name):
    ###write properties
    with open(file_name, 'a') as f:
        for ele in list(classList):
            f.write(ele + '\n')

        f.close()


def classExtractor(file_name):
    classesList = []
    classesP31 = []
    superClasses = []
    counter = 0

    # open dumps
    with bz2.BZ2File(file_name, 'r') as f:

        for line in f:
            try:
                lineParsed = ujson.loads(line[:-2])

                if counter % 100000 == 0:
                    print(counter, " items processed")
                    classesList = set(classesList)
                    classesP31 = set(classesP31)
                    writeClasslist(classesList, 'classesP279.txt')
                    writeClasslist(classesP31, 'classesP31.txt')
                    classesList = []
                    classesP31 = []

                # if 'P279' in lineParsed['claims'].keys():
                try:
                    entityID = lineParsed['id']
                    classesList.append(entityID)
                    for i in lineParsed['claims']['P279']:
                        if 'qualifiers' not in i.keys():
                            try:
                                superClass = i['mainsnak']['datavalue']['value']['id']
                                superClasses.append(superClass)
                                counter += 1
                            except:
                                print(i)
                except:
                    print('no class')

                # elif 'P31' in lineParsed['claims'].keys():
                try:
                    for i in lineParsed['claims']['P31']:
                        if 'qualifiers' not in i.keys():
                            try:
                                superClass = i['mainsnak']['datavalue']['value']['id']
                                classesP31.append(superClass)
                            except:
                                print(i)
                except:
                    print('no class')
            except:
                print(line)

    return [superClasses, classesList, classesP31]


def main():
    file_name = sys.argv[1]
    classesAll = classExtractor(file_name)
    classP279 = set(classesAll[1])
    classP31 = set(classesAll[2])
    superclasses = set(classesAll[0])

    #write files
    writeClasslist(classP279, 'classesP279_new.txt')
    writeClasslist(classP31, 'classesP31_new.txt')
    writeClasslist(superclasses, 'superclasses_new.txt')


if __name__ == "__main__":
    main()