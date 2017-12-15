#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime


class OntologyFile:

    def __init__(self, outputFile, fileType):
        self.fileType = fileType
        self.output = outputFile


        if self.fileType == 'rdf/owl':
            self.ontoWriter()
        elif self.fileType == 'rdf':
            self.dumpWriter()
        elif self.fileType == 'ttl':
            self.ttlWriter()


    def ontoWriter(self):

            self.output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            self.output.write('<rdf:RDF\n')
            self.output.write('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
            self.output.write('xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n')
            self.output.write('xmlns:owl="http://www.w3.org/2002/07/owl#"\n')
            self.output.write('xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
            self.output.write('xmlns:dcterms="http://purl.org/dc/terms/"\n')
            self.output.write('xmlns:d0="http://www.ontologydesignpatterns.org/ont/d0.owl#"\n')
            self.output.write('xmlns:dul="http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#"\n')
            self.output.write('xmlns:schema="http://schema.org/"\n')
            self.output.write('xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n')
            self.output.write('xmlns:wd="http://www.wikidata.org/entity/"\n')
            self.output.write('xmlns:wdt="http://www.wikidata.org/prop/direct/"\n')
            self.output.write('xmlns:wikibase="http://wikiba.se/ontology#">\n')

            self.output.write('<!-- OWL Header -->\n')
            self.output.write('<owl:Ontology rdf:about="http://myWikidataOntology">\n')
            self.output.write('<dc:title>Wikidata ontology</dc:title>\n')
            self.output.write('<rdfs:comment rdf:datatype = "http://www.w3.org/2001/XMLSchema#string">OWL ontology extracted from Wikidata dumps</rdfs:comment>\n')
            self.output.write('<owl:versionInfo> v.' + str(datetime.datetime.now()) + '</owl:versionInfo>\n')
            self.output.write('<owl:imports rdf:resource="http://wikiba.se/ontology-1.0.owl"/>\n')
            self.output.write('</owl:Ontology>\n')

    def dumpWriter(self):

            self.output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            self.output.write('<rdf:RDF\n')
            self.output.write('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
            self.output.write('xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n')
            self.output.write('xmlns:owl="http://www.w3.org/2002/07/owl#"\n')
            self.output.write('xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
            self.output.write('xmlns:dcterms="http://purl.org/dc/terms/"\n')
            self.output.write('xmlns:d0="http://www.ontologydesignpatterns.org/ont/d0.owl#"\n')
            self.output.write('xmlns:dul="http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#"\n')
            self.output.write('xmlns:schema="http://schema.org/"\n')
            self.output.write('xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n')
            self.output.write('xmlns:wd="http://www.wikidata.org/entity/"\n')
            self.output.write('xmlns:wdt="http://www.wikidata.org/prop/direct/"\n')
            self.output.write('xmlns:wikibase="http://wikiba.se/ontology#">\n')
            self.output.write('<!-- Data start here -->\n')


    def ttlWriter(self):
        self.output.write('@prefix dbp: <http://dbpedia.org/ontology/> .\n')
        self.output.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
        self.output.write('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n')
        self.output.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
        self.output.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
        self.output.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n')


    def finalWriter(self, propertyAll):
    ###WRITE PROPERTY FILE
        propertyTranslated = '\n'.join(propertyAll)
        self.output.write(propertyTranslated)
        self.output.write('\n</rdf:RDF>')
        self.output.close()

    def secondWriter(self, mappings):
        ### writes mapping files
        mappingLines = '\n'.join(mappings)
        self.output.write(mappingLines)
        self.output.close()


def classesReader(fileName):
    classesList = []
    with open(fileName, 'r') as f:
        for line in f:
            classesList.append(line.replace('\n', ''))

    classesList = set(classesList)
    print(len(classesList))
    return classesList