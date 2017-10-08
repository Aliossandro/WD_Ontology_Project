#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime


class OntologyFile:

    def __init__(self, outputFile):

        self.output = outputFile
        # self.dataFilter = dataFilter
        # self.propertyTypes = {}
        # self.propertyDeclarationQueue = []
        # self.filterName = self.dataFilter.getHashCode()
        # # Keep some statistics (inserted at end of file):
        # self.entityCount = 0
        # self.propertyCount = 0  # number of OWL property declarations, not of Wikidata properties
        # self.propertyLookupCount = 0  # number of additional online lookups
        # self.statStatementCount = 0
        # self.statReferenceCount = 0
        # self.statStmtPropertyCounts = {}
        # self.statStmtTypeCounts = {}
        # self.statQualiPropertyCounts = {}
        # self.statQualiTypeCounts = {}
        # self.statRefPropertyCounts = {}
        # self.statRefTypeCounts = {}
        # self.statTripleCount = 0

        # Make header:
        #self.output.write('### Wikidata OWL/RDF Ontology\n')
        # self.output.write('# Filter settings (' + self.filterName + ')\n')
        # for infostr in self.dataFilter.getFilterSettingsInfo():
        #     self.output.write('# - ' + infostr + '\n')

        #self.output.write('# Generated on ' + str(datetime.datetime.now()) + '\n###\n\n')

        self.output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.output.write('<rdf:RDF\n')
        self.output.write('xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
        self.output.write('xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n')
        self.output.write('xmlns:owl="http://www.w3.org/2002/07/owl#"\n')
        self.output.write('xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
        self.output.write('xmlns:dcterms="http://purl.org/dc/terms/"\n')
        self.output.write('xmlns:d0="http://www.ontologydesignpatterns.org/ont/d0.owl#"\n')
        self.output.write('xmlns:schema="http://schema.org/""\n')
        self.output.write('xmlns:wikibase="http://wikiba.se/ontology#"\n')
        self.output.write('xmlns:wd="<http://www.wikidata.org/entity/">\n')
        self.output.write('<!-- OWL Header -->\n')
        self.output.write('<owl:Ontology rdf:about="http://www.wikidata.org"\n')
        self.output.write('xmlns:xsd="http://www.w3.org/2001/XMLSchema#">\n')
        self.output.write('<dc:title>Wikidata ontology</dc:title>\n')
        self.output.write('<dc:description>OWL ontology extracted from Wikidata dumps</dc:description>\n')
        self.output.write('</owl:Ontology>\n\n')

    def finalWriter(self, propertyAll):
    ###WRITE PROPERTY FILE
        propertyTranslated = '\n'.join(propertyAll)
        self.output.write(propertyTranslated)
        self.output.write('</rdf:RDF>\n')
        self.output.close()