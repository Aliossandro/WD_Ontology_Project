import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class dbpediaQuery(object):

    def __init__(self, WDItem):
        self.WDItem    = WDItem
        self.values = self.getValues()

    def getValues(self):
        query = "select DISTINCT ?s where { \
            ?s owl:sameAs " + self.WDItem + ". }"

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        valueJoined = '\n'.join(self.createValuesObject(results["results"]["bindings"], self.WDItem))
        return valueJoined

    def createValuesObject(self, results, WDItem):
        valuesObjectList = []
        for result in results:
            sValue = result["s"]["value"]
            valuesObject = WDItem + ' <http://www.w3.org/2002/07/owl#sameAs> <' + sValue + '>'
            valuesObjectList.append(valuesObject)

        return valuesObjectList

class fileHandler(object):

    def __init__(self, fileIn, fileOut):
        self.fileIn = fileIn
        self.fileOut = fileOut
        self.sameAsList = self.fileOpener()
        self.fileWriter(self.sameAsList)

    def fileOpener(self):
        resultList = []
        with open(self.fileIn, 'r') as f:
            for line in f:
                WDItem = line.split(' ')[0]
                x = dbpediaQuery(WDItem)
                results = x.values
                if results not in resultList:
                    resultList.append(results)
        return resultList

    def fileWriter(self, results):
        with open(self.fileOut, 'w') as f:
            for item in results:
                f.write("%s\n" % item)
        f.close()


def main():
    file_name = sys.argv[1]
    file_output = sys.argv[2]
    x = fileHandler(file_name, file_output)

if __name__ == "__main__":
    main()