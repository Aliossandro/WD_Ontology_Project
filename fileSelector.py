import ujson
import re
import bz2
import os
import sys

###classes list generator
def classesGenerator(**args):
    classesList = []
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'classes.json'), 'r') as f:
        resultClasses = ujson.load(f)
        for binding in resultClasses['results']['bindings']:
            classUri = binding['cl']['value']
            if classUri[0:31] == 'http://www.wikidata.org/entity/':
                classId = classUri[31:]
                classesList.append(classId)
    print(len(classesList))
    return classesList

def classesReader(fileName):
    classesList = []
    with open(fileName, 'r') as f:
        for line in f:
            classesList.append(line.replace('\n', ''))

    classesList = set(classesList)
    print(len(classesList))
    return classesList

def writeClasslist(classList, file_name):
    ###write properties
    with open(file_name, 'a') as f:
        for ele in list(classList):
            f.write(ele + '\n')

        f.close()

def fileAnalyser(file_name, classFile):
    #load classes list
    classesList = classesReader(classFile)
    # classesList = classesGenerator()
    entitiesAll = []
    counter = 0
    # collect other properties


    # open dumps
    with bz2.BZ2File(file_name, 'r') as f:
        # counterI = 0
        # counterP = 0

        for line in f:
            # print(counter)

            if counter == 3000:
                writeClasslist(entitiesAll, 'classesMinList.json')
                entitiesAll = []
                counter = 0


            matcho = re.search(r'\{\"type\"\:\"item\"\,\"id\"\:\"[Qq][0-9]{1,}', str(line))
            if not matcho:
                entitiesAll.append(str(line))
                counter += 1

            else:
                sea = re.search(r'[Qq][0-9]{1,}', matcho.group(0))
                if sea.group(0) in classesList:
                    entitiesAll.append(str(line))
                    counter += 1

    return entitiesAll

def main():
    file_name = sys.argv[1]
    classFile = sys.argv[2]
    classesAll = fileAnalyser(file_name, classFile)

    #write files
    writeClasslist(classesAll, 'classesMinList.json')


if __name__ == "__main__":
    main()