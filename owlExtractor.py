#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson
import re
import bz2
import os
import fileWriter

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

def resourceNamer(resource):
    resourceUri = "http://www.wikidata.org/entity/" + resource

    return resourceUri

def rangeLine(resource):
    if resource != 'owl:Class':
        resourceUri = resourceNamer(resource)
    else:
        resourceUri = resource

    rangeOutput = '<rdfs:range rdf:resource="' + resourceUri + '"/>'

    return rangeOutput

def rangeMultiple(resource):
    if resource != 'owl:Class':
        resourceUri = resourceNamer(resource)
    else:
        resourceUri = resource

    rangeOutput = '<owl:Class rdf:resource="' + resourceUri + '"/>'

    return rangeOutput

def domainLine(resource):
    if resource != 'owl:Class':
        resourceUri = resourceNamer(resource)
    else:
        resourceUri = resource

    domainOutput = '<rdfs:domain rdf:resource="' + resourceUri + '"/>'

    return domainOutput

def collectionItems(resource):
    individualUri = resourceNamer(resource)
    individualOutput = '<owl:Thing rdf:about="' + individualUri + '"/>'

    return individualOutput

def disjointUnionClasses(object):
    disjointUnionOf = "http://www.wikidata.org/entity/" + object
    resourceDisjointUnionOf = '<owl:Class rdf:resource="' + disjointUnionOf + '"/>'

    return resourceDisjointUnionOf




###property extractor
class entityExtractor:

    def __init__(self, lineParsed):
        self.lineParsed = lineParsed



def propertyExtractor(lineParsed):
    otherKeys = []
    constraintKeys = []
    functional = False
    inverseFunctional = False
    symmetric = False
    conflictsWith = []

    try:
        resourceName = resourceNamer(lineParsed['id'])
    except:
        print(lineParsed)

    if lineParsed['datatype'] == 'wikibase-item':
        propertyType = "ObjectProperty"
    else:
        propertyType = "DatatypeProperty"

    propertyDeclaration = '<owl:' + propertyType + ' rdf:about="' + resourceName + '">'
    propertyDeclarationClosure = '</owl:' + propertyType + '>'
    resourceType = '<rdf:type rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"/>'
    resourceType2 = '<rdf:type rdf:resource="http://wikiba.se/ontology-beta#Property"/>'
    try:
        resourceLabel = '<rdfs:label xml:lang="en">' + lineParsed['labels']['en']['value'] + '</rdfs:label>'
    except KeyError:
        resourceLabel = '<rdfs:label xml:lang="en">no English label available</rdfs:label>'

    try:
        resourceDescription = '<schema:description xml:lang="en">' + lineParsed['descriptions']['en'][
            'value'] + '</schema:description>'
    except KeyError:
        resourceDescription = '<schema:description xml:lang="en">no English description available</schema:description>'

    # analyse claims
    # print(lineParsed['claims'].keys())
    for key in lineParsed['claims']:
        if key == 'P31':
            resourceInstanceList = []
            for i in lineParsed['claims']['P31']:
                instanceOf = i['mainsnak']['datavalue']['value']['id']
                instanceOf = "http://www.wikidata.org/entity/" + instanceOf
                resourceInstanceOf = '<rdf:type rdf:resource="' + instanceOf + '"/>'
                resourceInstanceList.append(resourceInstanceOf)

        elif key == 'P1659':
            resourceSeeList = []
            for i in lineParsed['claims']['P1659']:
                seeAlso = i['mainsnak']['datavalue']['value']['id']
                seeAlso = "http://www.wikidata.org/entity/" + seeAlso
                resourceSeeAlso = '<rdfs:seeAlso rdf:resource="' + seeAlso + '"/>'
                resourceSeeList.append(resourceSeeAlso)

        elif key == 'P1647':
            resourceSubPropertyList = []
            for i in lineParsed['claims']['P1647']:
                subPropertyOf = i['mainsnak']['datavalue']['value']['id']
                subPropertyOf = "http://www.wikidata.org/entity/" + subPropertyOf
                resourceSubPropertyOf = '<rdfs:subPropertyOf rdf:resource="' + subPropertyOf + '"/>'
                resourceSubPropertyList.append(resourceSubPropertyOf)

        elif key == 'P1628':
            resourceEquivalentList = []
            for i in lineParsed['claims']['P1628']:
                try:
                    equivalentProperty = i['mainsnak']['datavalue']['value']['id']
                    equivalentProperty = "#" + equivalentProperty
                except TypeError:
                    equivalentProperty = i['mainsnak']['datavalue']['value']

                resourceEquivalentProperty = '<owl:equivalentProperty rdf:resource="' + equivalentProperty + '"/>'
                resourceEquivalentList.append(resourceEquivalentProperty)

        elif key == 'P1696':
            resourceInverseList = []
            for i in lineParsed['claims']['P1696']:
                try:
                    inverseProperty = i['mainsnak']['datavalue']['value']['id']
                    inverseProperty = "#" + inverseProperty
                except TypeError:
                    inverseProperty = i['mainsnak']['datavalue']['value']

                resourceInverseProperty = '<owl:inverseOf rdf:resource="' + inverseProperty + '"/>'
                resourceInverseList.append(resourceInverseProperty)

        # elif key == 'P3254':
        #
        # elif key == 'P1793': ###format as regex

        ###property constraints
        elif key == 'P2302':
            constraintList = []
            for i in lineParsed['claims']['P2302']:
                # print(i['mainsnak']['datavalue']['value']['id'], resourceName)
                constraintKeys.append(i['mainsnak']['datavalue']['value']['id'])

                # Q21510865 'value type', range
                if i['mainsnak']['datavalue']['value']['id'] == 'Q21510865':
                    domainList = []
                    relation = [x['datavalue']['value']['id'] for x in i['qualifiers']['P2309']]
                    # Q21503252 instance of for constraints
                    if len(relation) == 1:
                        relation = relation[0]
                        if relation == 'Q21503252':
                            rangeTemp = '<rdfs:range rdf:resource="'
                        else:
                            print(relation, 'relation type')
                            # check if other qualifiers are used; what to do with them?
                            # break
                    else:
                        print(relation, 'relation type')
                        # check if there are other qualifiers; what to do with them?
                        # break

                    classRange = [y['datavalue']['value']['id'] for y in i['qualifiers']['P2308']]
                    # classRange = map(rangeLine, classRange)
                    # constraintList += list(classRange)

                # Q21503250 'type', domain
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21503250':
                    relation = [x['datavalue']['value']['id'] for x in i['qualifiers']['P2309']]
                    # Q21503252 instance of for constraints
                    if len(relation) == 1:
                        relation = relation[0]
                        if (relation == 'Q21503252') or (relation == 'Q30208840'):
                            rangeTemp = '<rdfs:domain rdf:resource="'
                        elif relation == 'Q21514624':
                            #add subclass
                            print(relation)
                        else:
                            print(relation, 'relation type')
                            # check if other qualifiers are used; what to do with them?
                            # break
                    else:
                        print(relation, 'relation type')
                        # check if there are other qualifiers; what to do with them?
                        # break

                    if 'P2308' in i['qualifiers'].keys():
                        classDomain = []
                        for y in i['qualifiers']['P2308']:
                            if y['datavalue']['value']['id'] == 'Q5127848':
                                classDomain.append('owl:Class')
                            else:
                                try:
                                    classDomain.append(y['datavalue']['value']['id'])
                                except:
                                    print(y)
                    else:
                        print(i['qualifiers'].keys())
                    # classDomain = map(domainLine, classDomain)
                    # constraintList += list(classDomain)

                # Q21510851 "allowed qualifiers" constraint ### what to do with it?



                # Q21502838 "conflicts-with" constraint
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21502838':
                    propertyConflicts = [x['datavalue']['value']['id'] for x in i['qualifiers']['P2306']]
                    if 'P2305' in i['qualifiers'].keys():
                        try:
                            conflictingObjects = [x['datavalue']['value']['id'] if x['snaktype'] == 'value' else 'somevalue' for x in i['qualifiers']['P2305']]

                            if propertyConflicts[0] == 'P31':
                                for obj in conflictingObjects:
                                    obj = '<owl:Class> \n<owl:complementOf rdf:resource="http://www.wikidata.org/entity/' + obj + '" /> \n</owl:Class>'
                                    conflictsWith.append(obj)
                            else:
                                for obj in conflictingObjects:
                                    obj = '<owl:Class> \n<owl:complementOf>\n<owl:Restriction>\n<owl:onProperty rdf:resource="http://www.wikidata.org/entity/' + propertyConflicts[0] + '" />\n<owl:hasValue rdf:resource ="http://www.wikidata.org/entity/' + obj + '" /> \n</owl:Restriction>\n</owl:complementOf>\n</owl:Class>'
                                    conflictsWith.append(obj)
                        except:
                            print(i['qualifiers']['P2305'])

                    else:
                        obj = '<owl:Class> \n<owl:complementOf>\n<owl:Restriction>\n<owl:onProperty rdf:resource="http://www.wikidata.org/entity/' + propertyConflicts[0] + '" />\n<owl:someValuesFrom rdf:resource="&owl;Thing" /> \n</owl:Restriction>\n</owl:complementOf>\n</owl:Class>'
                        conflictsWith.append(obj)



                # Q21510859 "one-of" constraint ###owl:oneOf: subject must be class, object must be list
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510859':
                    classOneOf = []
                    for y in i['qualifiers']['P2305']:
                        try:
                            classOneOf.append(y['datavalue']['value']['id'])
                            ###it can be 'no value' in snaktype
                        except:
                            print(i['qualifiers']['P2305'])
                    classOneOf = map(collectionItems, classOneOf)
                    # try:
                    #     classOneOf = [y['datavalue']['value']['id'] for y in i['qualifiers']['P2305']]
                    #     classOneOf = map(collectionItems, classOneOf)
                    # except:
                    #     print(i['qualifiers']['P2305'])


                   # Q25796498 "contemporary constraint: subject and object must exist at the same point in time; How do we specify that?

                # Q21502410; inverse functional property
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21502410':
                    inverseFunctional = True

                # Q19474404; functional property
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21502410':
                    functional = True

                # Q21510862 symmetric constraint
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510862':
                    symmetric = True

                # Q21510860; range constraint
                elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510860':
                    rangeDatatypeList = [' <rdfs:range>\n<rdfs:Datatype>']

                    if ('P2313' in i['qualifiers'].keys()) or ('P2312' in i['qualifiers'].keys()):
                        rangeDatatypeList.append('<owl:onDatatype rdf:resource="http://www.w3.org/2001/XMLSchema#decimal" />\n<owl:withRestrictions rdf:parseType="Collection">')
                        # min value
                        if 'P2313' in i['qualifiers'].keys():

                            for x in i['qualifiers']['P2312']:
                                if x['datatype'] == 'quantity':
                                    minRange = '<rdf:Description>\n<xsd:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + x['datavalue']['value']['amount'] + '</xsd:minInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(minRange)
                                else:
                                    print(x['datatype'])

                        #max value
                        elif 'P2312' in i['qualifiers'].keys():
                            for x in i['qualifiers']['P2312']:
                                if x['datatype'] == 'quantity':
                                    maxRange = '<rdf:Description>\n<xsd:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + \
                                               x['datavalue']['value']['amount'] + '</xsd:maxInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(maxRange)
                                else:
                                    print(x['datatype'])

                        closure = '</owl:withRestrictions>\n</rdfs:Datatype>\n</rdfs:range>'
                        rangeDatatypeList.append(closure)

                    elif ('P2311' in i['qualifiers'].keys()) or ('P2310' in i['qualifiers'].keys()):
                        rangeDatatypeList.append(
                            '<owl:onDatatype rdf:resource="http://www.w3.org/2001/XMLSchema#dateTime" />\n<owl:withRestrictions rdf:parseType="Collection">')
                        # max date
                        if 'P2311' in i['qualifiers'].keys():

                            for x in i['qualifiers']['P2311']:
                                if x['datatype'] == 'time':
                                    minRange = '<rdf:Description>\n<xsd:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' + \
                                               x['datavalue']['value'][
                                                   'time'] + '</xsd:maxInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(minRange)
                                else:
                                    print(x['datatype'])

                        # min date
                        elif 'P2310' in i['qualifiers'].keys():
                            for x in i['qualifiers']['P2310']:
                                if x['datatype'] == 'time':
                                    maxRange = '<rdf:Description>\n<xsd:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' + \
                                               x['datavalue']['value'][
                                                   'time'] + '</xsd:minInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(maxRange)
                                else:
                                    print(x['datatype'])

                        closure = '</owl:withRestrictions>\n</rdfs:Datatype>\n</rdfs:range>'
                        rangeDatatypeList.append(closure)

            if 'classRange' in locals():
                if len(list(classRange)) > 1:
                    classRange = map(rangeMultiple, classRange)
                    rangeClasses = '\n'.join(list(classRange))
                    if 'classOneOf' in locals():
                        oneOfCollection = '\n'.join(list(classOneOf))
                        oneOfCollection = '<owl:Class>\n<owl:oneOf rdf:parseType="Collection">\n' + oneOfCollection + '\n</owl:oneOf>\n</owl:Class>'
                        rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n' + oneOfCollection + '\n</owl:unionOf>\n</own:Class>\n</rdfs:range>'
                    else:
                        rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n</owl:unionOf>\n</own:Class>\n</rdfs:range>'
                else:
                    rangeInfo = list(map(rangeLine, classRange))
                    rangeInfo = '\n'.join(list(rangeInfo))

            # constraintList += list(rangeInfo)

            if 'classDomain' in locals():
                if len(list(classDomain)) > 1:
                    classDomain = map(rangeMultiple, classDomain)
                    domainClasses = '\n'.join(list(classDomain))
                    # if classOneOf:
                    #     oneOfCollection = '\n'.join(list(classOneOf))
                    #     oneOfCollection = '<owl:Class>\n<owl:oneOf rdf:parseType="Collection">\n' + oneOfCollection + '\n</owl:oneOf>\n</owl:Class>'
                    #     rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n' + oneOfCollection + '\n</owl:unionOf>\n</own:Class>\n</rdfs:range>'
                    # else:
                    domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + domainClasses + '\n</owl:unionOf>\n</own:Class>\n</rdfs:domain>'
                    if conflictsWith:
                        conflictList = '\n'.join(list(conflictsWith))
                        domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + domainClasses + '\n</owl:unionOf>\n</own:Class>\n'+ conflictList +'\n</owl:intersectionOf>\n</own:Class>\n</rdfs:domain>'

                else:
                    if conflictsWith:
                        conflictList = '\n'.join(list(conflictsWith))
                        domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n<owl:Class rdf:about="http://www.wikidata.org/entity/' + classDomain[0] + '"/>\n' + conflictList + '\n</owl:intersectionOf>\n</own:Class>\n</rdfs:domain>'

                    else:
                        domainInfo = list(map(domainLine, classDomain))
                        domainInfo = '\n'.join(list(domainInfo))
            else:
                if conflictsWith:
                    conflictList =  '\n'.join(list(conflictsWith))
                    domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n' + conflictList + '\n</owl:intersectionOf>\n</own:Class>\n</rdfs:domain>'

        else:
            otherKeys.append(key)

    # constraintList += list(domainInfo)
    propertyDescription = [propertyDeclaration, resourceLabel, resourceDescription, resourceType, resourceType2]
    if 'resourceInstanceList' in locals():
        resourceInstanceOf = '\n'.join(resourceInstanceList)
        propertyDescription.append(resourceInstanceOf)
    if 'resourceSeeList' in locals():
        resourceSeeAlso = '\n'.join(resourceSeeList)
        propertyDescription.append(resourceSeeAlso)
    if 'resourceSubPropertyList' in locals():
        resourceSubPropertyOf = '\n'.join(resourceSubPropertyList)
        propertyDescription.append(resourceSubPropertyOf)
    if 'resourceEquivalentList' in locals():
        resourceEquivalentProperty = '\n'.join(resourceEquivalentList)
        propertyDescription.append(resourceEquivalentProperty)
    if inverseFunctional:
        propertyDescription.append('<rdf:type rdf:resource="&owl;InverseFunctionalProperty" />')
    if functional:
        propertyDescription.append('<rdf:type rdf:resource="&owl;FunctionalProperty" />')
    if symmetric:
        propertyDescription.append('<rdf:type rdf:resource="&owl;SymmetricProperty" />')
    if 'domainInfo' in locals():
        propertyDescription.append(domainInfo)
    if 'rangeInfo' in locals():
        propertyDescription.append(rangeInfo)

    propertyDescription.append(propertyDeclarationClosure)

    return propertyDescription, otherKeys, constraintKeys

def classExtractor(lineParsed):
    otherKeys = []

    try:
        resourceName = resourceNamer(lineParsed['id'])
    except:
        print(lineParsed)


    classDeclaration = '<owl:Class rdf:about="' + resourceName + '">'
    classDeclarationClosure = '</owl:Class>'

    try:
        resourceLabel = '<rdfs:label xml:lang="en">' + lineParsed['labels']['en']['value'] + '</rdfs:label>'
    except KeyError:
        resourceLabel = '<rdfs:label xml:lang="en">no English label available</rdfs:label>'

    try:
        resourceDescription = '<schema:description xml:lang="en">' + lineParsed['descriptions']['en'][
            'value'] + '</schema:description>'
    except KeyError:
        resourceDescription = '<schema:description xml:lang="en">no English description available</schema:description>'

    # analyse claims
    # print(lineParsed['claims'].keys())
    for key in lineParsed['claims']:
        if key == 'P31':
            resourceInstanceList = []
            for i in lineParsed['claims']['P31']:
                try:
                    instanceOf = i['mainsnak']['datavalue']['value']['id']
                    instanceOf = "http://www.wikidata.org/entity/" + instanceOf
                    resourceInstanceOf = '<rdf:type rdf:resource="' + instanceOf + '"/>'
                    resourceInstanceList.append(resourceInstanceOf)
                except:
                    print(i, "A")

        elif key == 'P279':
            resourceSubClassList = []
            for i in lineParsed['claims']['P279']:
                try:
                    subClassOf = i['mainsnak']['datavalue']['value']['id']
                    subClassOf = "http://www.wikidata.org/entity/" + subClassOf
                    resourceSubClassOf = '<rdfs:subClassOf rdf:resource="' + subClassOf + '"/>'
                    resourceSubClassList.append(resourceSubClassOf)
                except:
                    print(i, 'B')

        elif key == 'P1709': #equivalent class
            resourceEquivalentClassList = []
            for i in lineParsed['claims']['P1709']:
                try:
                    equivalentClass = i['mainsnak']['datavalue']['value']['id']
                    equivalentClass = "http://www.wikidata.org/entity/" + equivalentClass
                    resourceEquivalentClassOf = '<rdfs:subClassOf rdf:resource="' + equivalentClass + '"/>'
                    resourceEquivalentClassList.append(resourceEquivalentClassOf)
                except:
                    try:
                        equivalentClass = i['mainsnak']['datavalue']['value']
                        resourceEquivalentClassOf = '<rdfs:subClassOf rdf:resource="' + equivalentClass + '"/>'
                        resourceEquivalentClassList.append(resourceEquivalentClassOf)
                    except:
                        print(i, 'C')

        elif key == 'P527': #has part
            resourceHasPartList = []
            for i in lineParsed['claims']['P527']:
                try:
                    hasPart = i['mainsnak']['datavalue']['value']['id']
                    hasPart = "http://www.wikidata.org/entity/" + hasPart
                    resourcehasPart = '<dcterms:hasPart rdf:resource="' + hasPart + '"/>'
                    resourceHasPartList.append(resourcehasPart)
                except:
                    print(i, 'D')

        elif key == 'P361': #is part of
            resourceIsPartList = []
            for i in lineParsed['claims']['P361']:
                try:
                    isPart = i['mainsnak']['datavalue']['value']['id']
                    isPart = "http://www.wikidata.org/entity/" + isPart
                    resourceIsPart = '<dcterms:isPartOf rdf:resource="' + isPart + '"/>'
                    resourceIsPartList.append(resourceIsPart)
                except:
                    print(i, 'E')

        elif key == 'P2737': #UnionOf
            resourceUnionList = ['<owl:unionOf>']
            for j in lineParsed['claims']['P2737']:
                for x in j['qualifiers']['P642']:
                    try:
                        resourceUnionList.append(disjointUnionClasses(x['datavalue']['value']['id']))
                ###account for somevalue/no value
                    except:
                        print(lineParsed['claims'][key], 'F')
            resourceUnionList.append('</owl:unionOf>')

        elif key == 'P2738': #disjointUnionOf
            resourceDisjointUnionList = ['<owl:DisjointUnion>']
            for j in lineParsed['claims']['P2738']:
                for x in j['qualifiers']['P642']:
                    try:
                        resourceDisjointUnionList.append(disjointUnionClasses(x['datavalue']['value']['id']))
                ###account for somevalue/no value
                    except:
                        print(x, 'G')
            resourceDisjointUnionList.append('</owl:DisjointUnion>')



        else:
            otherKeys.append(key)

    classData = [classDeclaration, resourceLabel, resourceDescription]
    if 'resourceInstanceList' in locals():
        resourceInstanceOf = '\n'.join(resourceInstanceList)
        classData.append(resourceInstanceOf)
    if 'resourceSubClassList' in locals():
        resourceSubClassOf = '\n'.join(resourceSubClassList)
        classData.append(resourceSubClassOf)
    if 'resourceEquivalentClassList' in locals():
        resourceEquivalentClassOf = '\n'.join(resourceEquivalentClassList)
        classData.append(resourceEquivalentClassOf)


    classData.append(classDeclarationClosure)

    return classData, otherKeys

    # print(classDeclaration, classDeclarationClosure)


def fileAnalyser(file_name, classFile):
    #load classes list
    classesList = classesReader(classFile)
    # classesList = classesGenerator()
    entitiesAll = []
    # collect other properties
    otherKeys = []
    constraintKeys = []

    # open dumps
    with bz2.BZ2File(file_name, 'r') as f:
        # counterI = 0
        # counterP = 0

        for line in f:
            # print(counter)

            # if counterI == 3000 and counterP == 300:
            #     otherKeys = set(otherKeys)
            #     constraintKeys = set(constraintKeys)
            #     return entitiesAll, otherKeys, constraintKeys
            #     break

            try:
                lineParsed = ujson.loads(line[:-2])
                entityID = lineParsed['id']

                if re.match('[P][0-9]{1,}', entityID):
                    # print(entityID)
                    # lineParsed = lineParsed['entities'][propertyId]
                    # extract resource name
                    propertyData = propertyExtractor(lineParsed)

                    try:
                        propertyDescriptionLine = '\n'.join(propertyData[0])
                        entitiesAll.append(propertyDescriptionLine)
                        # counterP += 1
                    except TypeError:
                        print(propertyData[0])

                    otherKeys += propertyData[1]
                    constraintKeys += propertyData[2]

                elif entityID in classesList:
                    # print(entityID)
                    # if counterI == 3000:
                    #     pass
                    # else:
                    # lineParsed = lineParsed['entities']['Q5'] ###temporary
                    classData = classExtractor(lineParsed)
                    try:
                        classDescriptionLine = '\n'.join(classData[0])
                        entitiesAll.append(classDescriptionLine)
                        # counterI += 1
                    except TypeError:
                        print(classData[0])

                    otherKeys += classData[1]

            except ValueError:
                print(line)




        otherKeys = set(otherKeys)
        constraintKeys = set(constraintKeys)

        return entitiesAll, otherKeys, constraintKeys


def writeOntology(propertyAll):
    ###write properties
    with open('WDOntology.owl', 'w') as f:
        x = fileWriter.OntologyFile(f)
        x.finalWriter(propertyAll)

