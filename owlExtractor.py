#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

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

    rangeOutput = '<owl:Class rdf:about="' + resourceUri + '"/>'

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


def lineProcessor(lineParsed):
    entitiesAll = []
    # collect other properties
    otherKeys = []
    constraintKeys = []
    hasKeyList =[]

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

def propertyExtractor(lineParsed):
    otherKeys = []
    constraintKeys = []
    functional = False
    inverseFunctional = False
    symmetric = False
    conflictsWith = []
    hasKeyList = []

    try:
        resourceName = resourceNamer(lineParsed['id'])
    except:
        print(lineParsed, 'wrong')

    if lineParsed['datatype'] == 'wikibase-item' or lineParsed['datatype'] == 'wikibase-property':
        propertyType = "ObjectProperty"
    else:
        propertyType = "DatatypeProperty"

    propertyDeclaration = '<owl:' + propertyType + ' rdf:about="' + resourceName + '">'
    propertyDeclarationClosure = '</owl:' + propertyType + '>'
    # resourceType = '<rdf:type rdf:resource="http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"/>'
    resourceType2 = '<rdf:type rdf:resource="http://wikiba.se/ontology-beta#Property"/>'
    try:
        label = lineParsed['labels']['en']['value']
        label = label.replace('&', ' and ')
        label = label.replace('<', ' ')
        label = label.replace('>', ' ')
        resourceLabel = '<rdfs:label xml:lang="en">' + label + '</rdfs:label>'
    except KeyError:
        resourceLabel = '<rdfs:label xml:lang="en">no English label available</rdfs:label>'

    try:
        description = lineParsed['descriptions']['en']['value']
        description = description.replace('&', ' and ')
        description = description.replace('<', ' ')
        description = description.replace('>', ' ')
        resourceDescription = '<schema:description xml:lang="en">' + description + '</schema:description>'
    except KeyError:
        resourceDescription = '<schema:description xml:lang="en">no English description available</schema:description>'

    # analyse claims
    # print(lineParsed['claims'].keys())
    if 'P31' in lineParsed['claims'].keys():
        resourceInstanceList = []
    if 'P1659' in lineParsed['claims'].keys():
        resourceSeeList = []
    if 'P1647' in lineParsed['claims'].keys():
        resourceSubPropertyList = []
    if 'P1628' in lineParsed['claims'].keys():
        resourceEquivalentList = []
    if 'P1696' in lineParsed['claims'].keys():
        resourceInverseList = []
    if 'P2302' in lineParsed['claims'].keys():
        constraintList = []



    # for key in lineParsed['claims']:
        # if key == 'P31':
        #     resourceInstanceList = []
    ###try P31
    try:
        for i in lineParsed['claims']['P31']:
            if i['mainsnak']['datavalue']['value']['id'] == 'Q18647515': #Transitive property
                resourceInstanceOf = '<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#TransitiveProperty"/>'
                resourceInstanceList.append(resourceInstanceOf)
            elif i['mainsnak']['datavalue']['value']['id'] == 'Q18647519': #asymmetric property
                resourceInstanceOf = '<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#AsymmetricProperty"/>'
                resourceInstanceList.append(resourceInstanceOf)
            elif i['mainsnak']['datavalue']['value']['id'] == 'Q18647521': #reflexive property
                resourceInstanceOf = '<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#ReflexiveProperty"/>'
                resourceInstanceList.append(resourceInstanceOf)
            else:
                instanceOf = i['mainsnak']['datavalue']['value']['id']
                instanceOf = "http://www.wikidata.org/entity/" + instanceOf
                resourceInstanceOf = '<rdf:type rdf:resource="' + instanceOf + '"/>'
                resourceInstanceList.append(resourceInstanceOf)
    except KeyError:
        print('No P31')

        # elif key == 'P1659':
        #     resourceSeeList = []
    try:
        for i in lineParsed['claims']['P1659']:
            seeAlso = i['mainsnak']['datavalue']['value']['id']
            seeAlso = "http://www.wikidata.org/entity/" + seeAlso
            resourceSeeAlso = '<rdfs:seeAlso rdf:resource="' + seeAlso + '"/>'
            resourceSeeList.append(resourceSeeAlso)
    except KeyError:
        print('No P1659')

        # elif key == 'P1647':
        #     resourceSubPropertyList = []
    try:
        for i in lineParsed['claims']['P1647']:
            subPropertyOf = i['mainsnak']['datavalue']['value']['id']
            subPropertyOf = "http://www.wikidata.org/entity/" + subPropertyOf
            resourceSubPropertyOf = '<rdfs:subPropertyOf rdf:resource="' + subPropertyOf + '"/>'
            resourceSubPropertyList.append(resourceSubPropertyOf)
    except KeyError:
        print('No P1647')

        # elif key == 'P1628':
        #     resourceEquivalentList = []
    try:
        for i in lineParsed['claims']['P1628']:
            try:
                equivalentProperty = i['mainsnak']['datavalue']['value']['id']
                equivalentProperty = "#" + equivalentProperty
            except TypeError:
                equivalentProperty = i['mainsnak']['datavalue']['value']

            resourceEquivalentProperty = '<owl:equivalentProperty rdf:resource="' + equivalentProperty + '"/>'
            resourceEquivalentList.append(resourceEquivalentProperty)
    except KeyError:
        print('No P1628')

        # elif key == 'P1696':
        #     resourceInverseList = []
    try:
        for i in lineParsed['claims']['P1696']:
            try:
                inverseProperty = i['mainsnak']['datavalue']['value']['id']
                inverseProperty = "#" + inverseProperty
            except TypeError:
                inverseProperty = i['mainsnak']['datavalue']['value']

            resourceInverseProperty = '<owl:inverseOf rdf:resource="' + inverseProperty + '"/>'
            resourceInverseList.append(resourceInverseProperty)
    except KeyError:
        print('No P1696')

        # elif key == 'P3254':
        #
        # elif key == 'P1793': ###format as regex

        ###property constraints
        # elif key == 'P2302':
        #     constraintList = []
    try:
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
                                print(y, 'K')
                else:
                    print(i['qualifiers'].keys(), 'P')
                # classDomain = map(domainLine, classDomain)
                # constraintList += list(classDomain)
                    # Q21502410; inverse functional property

            elif i['mainsnak']['datavalue']['value']['id'] == 'Q21502410':
                inverseFunctional = True

                # Q19474404; functional property
            elif i['mainsnak']['datavalue']['value']['id'] == 'Q19474404':
                functional = True

            # Q21510862 symmetric constraint
            elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510862':
                symmetric = True

            # Q21510860; range constraint
            elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510860':
                rangeDatatypeList = ['<rdfs:range>\n<rdfs:Datatype>']

                if ('P2313' in i['qualifiers'].keys()) or ('P2312' in i['qualifiers'].keys()):
                    rangeDatatypeList.append(
                        '<owl:onDatatype rdf:resource="http://www.w3.org/2001/XMLSchema#decimal" />\n<owl:withRestrictions rdf:parseType="Collection">')
                    # min value
                    try:
                        for x in i['qualifiers']['P2313']:
                            if x['datatype'] == 'quantity' and x['snaktype'] is not 'somevalue':
                                value = x['datavalue']['value']['amount']
                                if '.' not in str(value):
                                    minRange = '<rdf:Description>\n<xsd:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + value + '</xsd:minInclusive>\n</rdf:Description>'
                                else:
                                    minRange = '<rdf:Description>\n<xsd:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + value + '</xsd:minInclusive>\n</rdf:Description>'
                                rangeDatatypeList.append(minRange)
                            else:
                                print(x['datatype'], 'N')
                    except:
                        print('no P2313')

                    # max value
                    try:
                        for x in i['qualifiers']['P2312']:
                            if x['datatype'] == 'quantity' and x['snaktype'] is not 'somevalue':
                                value = x['datavalue']['value']['amount']
                                if '.' not in str(value):
                                    maxRange = '<rdf:Description>\n<xsd:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + value + '</xsd:maxInclusive>\n</rdf:Description>'
                                else:
                                    maxRange = '<rdf:Description>\n<xsd:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + value + '</xsd:maxInclusive>\n</rdf:Description>'
                                rangeDatatypeList.append(maxRange)
                            else:
                                print(x['datatype'], 'M')
                    except:
                        print('no P2312')

                    closure = '</owl:withRestrictions>\n</rdfs:Datatype>\n</rdfs:range>'
                    rangeDatatypeList.append(closure)

                elif ('P2311' in i['qualifiers'].keys()) or ('P2310' in i['qualifiers'].keys()):
                    rangeDatatypeList.append('<owl:onDatatype rdf:resource="http://www.w3.org/2001/XMLSchema#dateTime" />\n<owl:withRestrictions rdf:parseType="Collection">')
                    # min date
                    # if 'P2310' in i['qualifiers'].keys():
                    try:
                        for x in i['qualifiers']['P2310']:
                            if x['datatype'] == 'time' and x['snaktype'] is not 'somevalue':
                                try:
                                    value = x['datavalue']['value']['time']
                                    if str(value).startswith('+'):
                                        value = value.replace('+', '')
                                    value = value.replace('Z', '')
                                    maxRange = '<rdf:Description>\n<xsd:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' + \
                                               x['datavalue']['value'][
                                                   'time'] + '</xsd:minInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(maxRange)
                                except:
                                    print(x)
                            else:
                                print(x['datatype'], 'L')
                    except:
                        print('no P2310')
                    # max date
                    # elif 'P2311' in i['qualifiers'].keys():
                    try:
                        for x in i['qualifiers']['P2311']:
                            if x['datatype'] == 'time' and x['snaktype'] != 'somevalue':
                                try:
                                    value = x['datavalue']['value']['time']
                                    if str(value).startswith('+'):
                                        value = value.replace('+', '')
                                    value = value.replace('Z', '')
                                    minRange = '<rdf:Description>\n<xsd:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' + value + '</xsd:maxInclusive>\n</rdf:Description>'
                                    rangeDatatypeList.append(minRange)
                                except:
                                    print(x)
                            else:
                                print(x['datatype'], 'J')
                    except:
                        print('no P2311')


                    closure = '</owl:withRestrictions>\n</rdfs:Datatype>\n</rdfs:range>'
                    rangeDatatypeList.append(closure)


                    # Q21510851 "allowed qualifiers" constraint ### what to do with it?

            # Q21502838 "conflicts-with" constraint
            # elif i['mainsnak']['datavalue']['value']['id'] == 'Q21502838':
            #     propertyConflicts = [x['datavalue']['value']['id'] for x in i['qualifiers']['P2306']]
            #     if 'P2305' in i['qualifiers'].keys():
            #         conflictingObjects = []
            #         for x in i['qualifiers']['P2305']:
            #             if x['snaktype'] == 'value':
            #                 try:
            #                     conflictingObjects.append(x['datavalue']['value']['id'])
            #                 except:
            #                     print(i['qualifiers']['P2305'], 'H')
            #             elif x['snaktype'] == 'somevalue':
            #                 conflictingObjects.append('somevalue')
            #             elif x['snaktype'] == 'novalue':
            #                 conflictingObjects.append('novalue')
            #
            #         # try:
            #         #     conflictingObjects = [x['datavalue']['value']['id'] if x['snaktype'] == 'value' else 'somevalue' for x in i['qualifiers']['P2305']]
            #
            #         if propertyConflicts[0] == 'P31':
            #             for obj in conflictingObjects:
            #                 obj = '<owl:Class> \n<owl:complementOf rdf:resource="http://www.wikidata.org/entity/' + obj + '" /> \n</owl:Class>'
            #                 conflictsWith.append(obj)
            #         else:
            #             for obj in conflictingObjects:
            #                 obj = '<owl:Class> \n<owl:complementOf>\n<owl:Restriction>\n<owl:onProperty rdf:resource="http://www.wikidata.org/entity/' + propertyConflicts[0] + '" />\n<owl:hasValue rdf:resource ="http://www.wikidata.org/entity/' + obj + '" /> \n</owl:Restriction>\n</owl:complementOf>\n</owl:Class>'
            #                 conflictsWith.append(obj)
            #         # except:
            #         #     print(i['qualifiers']['P2305'])
            #
            #     else:
            #         obj = '<owl:Class> \n<owl:complementOf>\n<owl:Restriction>\n<owl:onProperty rdf:resource="http://www.wikidata.org/entity/' + propertyConflicts[0] + '" />\n<owl:someValuesFrom rdf:resource="http://www.w3.org/2002/07/owl#Thing" /> \n</owl:Restriction>\n</owl:complementOf>\n</owl:Class>'
            #         conflictsWith.append(obj)
            #
            # # Q21510859 "one-of" constraint ###owl:oneOf: subject must be class, object must be list
            # elif i['mainsnak']['datavalue']['value']['id'] == 'Q21510859':
            #     classOneOf = []
            #     for y in i['qualifiers']['P2305']:
            #         if y['snaktype'] != 'somevalue' or y['snaktype'] != 'novalue':
            #             try:
            #                 classOneOf.append(y['datavalue']['value']['id'])
            #                 ###it can be 'no value' in snaktype
            #             except:
            #                 print(y, 'O')#some issue here!!!
            #     classOneOf = map(collectionItems, classOneOf)
            #     # try:
            #     #     classOneOf = [y['datavalue']['value']['id'] for y in i['qualifiers']['P2305']]
            #     #     classOneOf = map(collectionItems, classOneOf)
            #     # except:
            #     #     print(i['qualifiers']['P2305'])
            #

               # Q25796498 "contemporary constraint: subject and object must exist at the same point in time; How do we specify that?
    except KeyError:
        print('no constraints')


    if 'classRange' in locals():
        if len(list(classRange)) > 1:
            classRange = map(rangeMultiple, classRange)
            rangeClasses = '\n'.join(list(classRange))
            if 'classOneOf' in locals():
                oneOfCollection = '\n'.join(list(classOneOf))
                oneOfCollection = '<owl:Class>\n<owl:oneOf rdf:parseType="Collection">\n' + oneOfCollection + '\n</owl:oneOf>\n</owl:Class>'
                rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n' + oneOfCollection + '\n</owl:unionOf>\n</owl:Class>\n</rdfs:range>'
            else:
                rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n</owl:unionOf>\n</owl:Class>\n</rdfs:range>'
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
            #     rangeInfo = '<rdfs:range>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + rangeClasses + '\n' + oneOfCollection + '\n</owl:unionOf>\n</owl:Class>\n</rdfs:range>'
            # else:
            domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + domainClasses + '\n</owl:unionOf>\n</owl:Class>\n</rdfs:domain>'
            if conflictsWith:
                conflictList = '\n'.join(list(conflictsWith))
                domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n<owl:Class>\n<owl:unionOf rdf:parseType="Collection">\n' + domainClasses + '\n</owl:unionOf>\n</owl:Class>\n'+ conflictList +'\n</owl:intersectionOf>\n</owl:Class>\n</rdfs:domain>'

        else:
            if conflictsWith:
                conflictList = '\n'.join(list(conflictsWith))
                domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n<owl:Class rdf:about="http://www.wikidata.org/entity/' + classDomain[0] + '"/>\n' + conflictList + '\n</owl:intersectionOf>\n</owl:Class>\n</rdfs:domain>'

            else:
                domainInfo = list(map(domainLine, classDomain))
                domainInfo = '\n'.join(list(domainInfo))
    else:
        if conflictsWith:
            conflictList =  '\n'.join(list(conflictsWith))
            domainInfo = '<rdfs:domain>\n<owl:Class>\n<owl:intersectionOf rdf:parseType="Collection">\n' + conflictList + '\n</owl:intersectionOf>\n</owl:Class>\n</rdfs:domain>'

        # else:
        #     otherKeys.append(key)

    # constraintList += list(domainInfo)
    propertyDescription = [propertyDeclaration, resourceLabel, resourceDescription, resourceType2]
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
        if propertyType == "DatatypeProperty":
            if 'classDomain' in locals():
                for item in classDomain:
                    hasKeyList.append((lineParsed['id'], item))
                    print((lineParsed['id'], item))
        else:
            propertyDescription.append('<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#InverseFunctionalProperty" />')
    if functional:
        propertyDescription.append('<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#FunctionalProperty" />')
    if symmetric:
        propertyDescription.append('<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#SymmetricProperty" />')
    if 'domainInfo' in locals():
        propertyDescription.append(domainInfo)
    if 'rangeInfo' in locals():
        propertyDescription.append(rangeInfo)
    if 'rangeDatatypeList' in locals():
        rangeDatatype = '\n'.join(rangeDatatypeList)
        propertyDescription.append(rangeDatatype)

    propertyDescription.append(propertyDeclarationClosure)

    return propertyDescription, otherKeys, constraintKeys, hasKeyList

def classExtractor(lineParsed, hasKey):
    otherKeys = []

    try:
        resourceName = resourceNamer(lineParsed['id'])
    except:
        print(lineParsed)


    classDeclaration = '<owl:Class rdf:about="' + resourceName + '">'
    classDeclarationClosure = '</owl:Class>'

    try:
        label = lineParsed['labels']['en']['value']
        label = label.replace('&', ' and ')
        label = label.replace('<', ' ')
        label = label.replace('>', ' ')
        resourceLabel = '<rdfs:label xml:lang="en">' + label + '</rdfs:label>'
    except KeyError:
        resourceLabel = '<rdfs:label xml:lang="en">no English label available</rdfs:label>'

    try:
        description = lineParsed['descriptions']['en']['value']
        description = description.replace('&', ' and ')
        description = description.replace('<', ' ')
        description = description.replace('>', ' ')
        resourceDescription = '<schema:description xml:lang="en">' + description + '</schema:description>'
    except KeyError:
        resourceDescription = '<schema:description xml:lang="en">no English description available</schema:description>'

    # analyse claims
    # print(lineParsed['claims'].keys())
    if 'P31' in lineParsed['claims'].keys():
        resourceInstanceList = []
    if 'P279' in lineParsed['claims'].keys():
        resourceSubClassList = []
    if 'P1709' in lineParsed['claims'].keys():
        resourceEquivalentClassList = []
    if 'P527' in lineParsed['claims'].keys():
        resourceHasPartList = []
    if 'P361' in lineParsed['claims'].keys():
        resourceIsPartList = []
    if 'P2737' in lineParsed['claims'].keys():
        resourceUnionList = ['<owl:unionOf>']
    if 'P2738' in lineParsed['claims'].keys():
        resourceDisjointUnionList = ['<owl:DisjointUnion>']

    # for key in lineParsed['claims']:

        # if key == 'P31':
        #     resourceInstanceList = []
    try:
        for i in lineParsed['claims']['P31']:
            if i['mainsnak']['snaktype'] == 'value':
                try:
                    instanceOf = i['mainsnak']['datavalue']['value']['id']
                    instanceOf = "http://www.wikidata.org/entity/" + instanceOf
                    resourceInstanceOf = '<rdf:type rdf:resource="' + instanceOf + '"/>'
                    resourceInstanceList.append(resourceInstanceOf)
                except:
                    print(i, "A")
    except:
        print('No P31')

        # elif key == 'P279':
        #     resourceSubClassList = []

    try:
        for i in lineParsed['claims']['P279']:
            if i['mainsnak']['snaktype'] == 'value':
                try:
                    subClassOf = i['mainsnak']['datavalue']['value']['id']
                    subClassOf = "http://www.wikidata.org/entity/" + subClassOf
                    resourceSubClassOf = '<rdfs:subClassOf rdf:resource="' + subClassOf + '"/>'
                    resourceSubClassList.append(resourceSubClassOf)
                except:
                    print(i, 'B')
    except:
        print('No P279')

        # elif key == 'P1709': #equivalent class
        #     resourceEquivalentClassList = []
    try:
        for i in lineParsed['claims']['P1709']:
            if i['mainsnak']['snaktype'] == 'value':
                try:
                    equivalentClass = i['mainsnak']['datavalue']['value']['id']
                    equivalentClass = "http://www.wikidata.org/entity/" + equivalentClass
                    resourceEquivalentClassOf = '<owl:equivalentClass rdf:resource="' + equivalentClass + '"/>'
                    resourceEquivalentClassList.append(resourceEquivalentClassOf)
                except:
                    try:
                        equivalentClass = i['mainsnak']['datavalue']['value']
                        resourceEquivalentClassOf = '<owl:equivalentClass rdf:resource="' + equivalentClass + '"/>'
                        resourceEquivalentClassList.append(resourceEquivalentClassOf)
                    except:
                        print(i, 'C')
    except:
        print('No P1709')

        # elif key == 'P527': #has part
        #     resourceHasPartList = []
    try:
        for i in lineParsed['claims']['P527']:
            if i['mainsnak']['snaktype'] == 'value':
                try:
                    hasPart = i['mainsnak']['datavalue']['value']['id']
                    hasPart = "http://www.wikidata.org/entity/" + hasPart
                    resourcehasPart = '<dcterms:hasPart rdf:resource="' + hasPart + '"/>'
                    resourceHasPartList.append(resourcehasPart)
                except:
                    print(i, 'D')
    except:
        print('No P527')

        # elif key == 'P361': #is part of
        #     resourceIsPartList = []
    try:
        for i in lineParsed['claims']['P361']:
            if i['mainsnak']['snaktype'] == 'value':
                try:
                    isPart = i['mainsnak']['datavalue']['value']['id']
                    isPart = "http://www.wikidata.org/entity/" + isPart
                    resourceIsPart = '<dcterms:isPartOf rdf:resource="' + isPart + '"/>'
                    resourceIsPartList.append(resourceIsPart)
                except:
                    print(i, 'E')
    except:
        print('No P361')

        # elif key == 'P2737': #UnionOf
        #     resourceUnionList = ['<owl:unionOf>']
    try:
        for j in lineParsed['claims']['P2737']:
            if 'qualifiers' in j.keys():
                for x in j['qualifiers']['P642']:
                    if x['snaktype'] == 'value':
                        try:
                            resourceUnionList.append(disjointUnionClasses(x['datavalue']['value']['id']))
                    ###account for somevalue/no value
                        except:
                            print(lineParsed['claims'][key], 'F')
        resourceUnionList.append('</owl:unionOf>')
    except:
        print('No P2737')

        # elif key == 'P2738': #disjointUnionOf
        #     resourceDisjointUnionList = ['<owl:DisjointUnion>']
    try:
        for j in lineParsed['claims']['P2738']:
            if 'qualifiers' in j.keys():
                for x in j['qualifiers']['P642']:
                    if x['snaktype'] == 'value':
                        try:
                            resourceDisjointUnionList.append(disjointUnionClasses(x['datavalue']['value']['id']))
                    ###account for somevalue/no value
                        except:
                            print(x, 'G')
        resourceDisjointUnionList.append('</owl:DisjointUnion>')
    except:
        print('No P2738')


    # else:
    #     otherKeys.append(key)

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
    if type(hasKey) is list:
        hasKeyObject = '<owl:hasKey rdf:parseType="Collection">'
        classData.append(hasKeyObject)
        for propertyId in hasKey:
            propertyKey = '<owl:DatatypeProperty rdf:about="http://www.wikidata.org/entity/' + propertyId + '" />'
            classData.append(propertyKey)
        classData.append('</owl:hasKey>')
    if 'resourceHasPartList' in locals():
        resourceHasPartList = '\n'.join(resourceHasPartList)
        classData.append(resourceHasPartList)
    if 'resourceIsPartList' in locals():
        resourceIsPartList = '\n'.join(resourceIsPartList)
        classData.append(resourceIsPartList)
    if 'resourceUnionList' in locals():
        resourceUnionList = '\n'.join(resourceUnionList)
        classData.append(resourceUnionList)
    if 'resourceDisjointUnionList' in locals():
        resourceDisjointUnionList = '\n'.join(resourceDisjointUnionList)
        classData.append(resourceDisjointUnionList)

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
    hasKeyTuples = []

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

            matcho = re.search(r'\{\"type\"\:\"item\"\,\"id\"\:\"[Qq][0-9]{1,}', str(line))
            if not matcho:
                try:
                    lineParsed = ujson.loads(line[:-2])

                # entityID = lineParsed['id']

                # if re.match('[P][0-9]{1,}', entityID):
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
                    hasKeyTuples += propertyData[3]


                except ValueError:
                    try:
                        line = line.replace('\n', '')
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
                            hasKeyTuples += propertyData[3]

                    except:
                        print(line)


        f.seek(0)
        hasKeyList = [item[1] for item in hasKeyTuples]
        print('start with items')
        print(hasKeyList)
        for line in f:
            matcho = re.search(r'\{\"type\"\:\"item\"\,\"id\"\:\"[Qq][0-9]{1,}', str(line))
            if matcho:
                sea = re.search(r'[Qq][0-9]{1,}', matcho.group(0))
                if sea.group(0) in classesList:
                    try:
                        lineParsed = ujson.loads(line[:-2])
                        entityID = lineParsed['id']

                        if entityID in classesList:
                            # print(entityID)
                            # if counterI == 3000:
                            #     pass
                            # else:
                            # lineParsed = lineParsed['entities']['Q5'] ###temporary
                            if entityID in hasKeyList:
                                propertyKeyList = [item[0] for item in hasKeyTuples if item[1] == entityID]
                                classData = classExtractor(lineParsed, propertyKeyList)
                            else:
                                classData = classExtractor(lineParsed, 0)
                            try:
                                classDescriptionLine = '\n'.join(classData[0])
                                entitiesAll.append(classDescriptionLine)
                                # counterI += 1
                            except TypeError:
                                print(classData[0])

                            otherKeys += classData[1]

                    except ValueError:
                        try:
                            line = line.replace('\n', '')
                            lineParsed = ujson.loads(line[:-2])
                            entityID = lineParsed['id']

                            if entityID in classesList:
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
                        except:
                            print(line)

        otherKeys = set(otherKeys)
        constraintKeys = set(constraintKeys)

        return entitiesAll, otherKeys, constraintKeys


def writeOntology(propertyAll):
    ###write properties
    with open('WDOntology.owl', 'w') as f:
        x = fileWriter.OntologyFile(f)
        x.finalWriter(propertyAll)

