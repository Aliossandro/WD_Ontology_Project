import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class dbpediaQuery(object):

    # def __init__(self):
    #
    #     #self.WDItem = WDItem
        # self.values = self.getValues()

    def dbFile(self, dbFile):
        self.dbAxiomList = []
        with open(dbFile, 'r') as f:
            for line in f:

                dbAxiom = line.split(' ')
                dbAxiom = dbAxiom[2].replace(' .', '')
                # self.Entity = dbAxiom
                self.getWeirdDb(dbAxiom)

    def dbWriter(self, fileOut):
        with open(fileOut, 'w') as f:
            for line in self.dbAxiomList:
                f.write(line)
            f.close()

    def getWeirdDb(self, dbEntity):
        query = "select ?o where { \
                    " + dbEntity + "  owl:sameAs  ?o. }"


        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        valueResults = self.sameAsObject(results["results"]["bindings"], dbEntity)

        if valueResults is not None:
            self.dbAxiomList.append(valueResults)
            # if len(valueResults) > 1:
            #     valuesJoined = '\n'.join(valueResults)
            #     print(valuesJoined)
            #     self.dbAxiomList.append(valuesJoined)
            #
            # else:
            #     self.dbAxiomList.append(valueResults[0])


        # return valueJoined

        queryType = "select ?o where { \
                            " + dbEntity + "  a  ?o. }"
        sparql.setQuery(queryType)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        valueResults = self.typeObject(results["results"]["bindings"], dbEntity)

        if valueResults is not None:
            try:
                valueJoined = '\n'.join(valueResults)
            except TypeError:
                print(valueResults)
            self.dbAxiomList.append(valueJoined)

    def equivalentDb(self, dbEntity):
        query = "select ?o where { \
                    <" + dbEntity + ">  owl:equivalentClass  ?o. }"


        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        valueResults = self.equivalentClass(results["results"]["bindings"], dbEntity)

        if valueResults is not None:
            return valueResults
        else:
            return None

    def subclassDb(self, dbEntity):
        query = "select ?o where { \
                    <" + dbEntity + ">  <http://www.w3.org/2000/01/rdf-schema#subClassOf>  ?o. }"


        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        valueResults = self.sameAsObject(results["results"]["bindings"], dbEntity)

        if valueResults is not None:
            return valueResults
        else:
            return None


    def sameAsObject(self, results, dbEntity):
        valuesObjectList = []
        for result in results:
            sValue = result["o"]["value"]
            if 'yago' in sValue:
                if '<' not in dbEntity:
                    valuesObject = '<' + dbEntity + '> <http://www.w3.org/2002/07/owl#sameAs> <' + sValue + '> .'
                    valuesObjectList.append(valuesObject)
                else:
                    valuesObject = dbEntity + ' <http://www.w3.org/2002/07/owl#sameAs> <' + sValue + '> .'
                    valuesObjectList.append(valuesObject)

        if len(valuesObjectList) > 0:
            valuesJoined = '\n'.join(valuesObjectList)
            return valuesJoined
        else:
            return None

    def typeObject(self, results, dbEntity):
        valuesObjectList = []
        for result in results:
            sValue = result["o"]["value"]
            if 'http://dbpedia.org/class/yago/' in sValue:
                valuesObject =   dbEntity + ' <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <' + sValue + '> .'
                valuesObjectList.append(valuesObject)
                valueEquivalent = self.equivalentDb(sValue)
                if valueEquivalent is not None:
                    valuesObjectList.append(valueEquivalent)
                valueSubclass = self.subclassDb(sValue)
                if valueSubclass is not None:
                    valuesObjectList.append(valueSubclass)

        if len(valuesObjectList) > 0:
            return valuesObjectList
        else:
            return None


    def equivalentClass(self, results, dbEntity):
        valuesObjectList = []
        for result in results:
            try:
                sValue = result["o"]["value"]

                valuesObject = '<' + dbEntity + '> <http://www.w3.org/2002/07/owl#equivalentClass> <' + sValue + '> .'
                valuesObjectList.append(valuesObject)

                if len(valuesObjectList) > 1:
                    valuesJoined = '\n'.join(valuesObjectList)
                    return valuesJoined
                else:
                    return valuesObjectList[0]
            except:
                return None

    def subClass(self, results, dbEntity):
        valuesObjectList = []
        for result in results:
            try:
                sValue = result["o"]["value"]

                valuesObject = '<' + dbEntity + '> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <' + sValue + '> .'
                valuesObjectList.append(valuesObject)
                if len(valuesObjectList) > 1:
                    valuesJoined = '\n'.join(valuesObjectList)
                    return valuesJoined
                else:
                    return valuesObjectList[0]
            except:
                return None

    def getValues(self, WDItem):
        self.WDItem = WDItem
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
                x = dbpediaQuery()
                x.getValues(WDItem)
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