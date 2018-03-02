import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class disjointCleaner(object):

    def __init__(self, fileIn, fileReplace, fileMappings):
        self.fileIn = fileIn
        self.fileReplace = fileReplace
        self.fileMap = fileMappings
        self.disjointListHolder()
        self.disjointRemove()
        self.cleanWriter()

    def disjointListHolder(self):
        disjointList = []
        with open(self.fileIn, 'r') as f:
            for line in f:
                disjointList.append(line)
        self.disjointList = disjointList

    def disjointRemove(self):
        cleanList = []
        with open(self.fileMap, 'r') as m:
            for line in m:
                if line not in self.disjointList:
                    cleanList.append(line)
        self.cleanList = cleanList

    def cleanWriter(self):
        with open(self.fileReplace, 'w') as n:
            for line in self.cleanList:
                n.write(line)
            n.close()



def main():
    file_name = sys.argv[1]
    file_map = sys.argv[2]
    file_output = sys.argv[3]
    disjointCleaner(file_name, file_output, file_map)


if __name__ == "__main__":
    main()