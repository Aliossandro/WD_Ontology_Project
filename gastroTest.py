#!/usr/bin/python
# -*- coding: utf-8 -*-

# import ujson
# import re
# import bz2
import os
import sys
import pandas as pd
# import urllib.parse
# import csv
# import seaborn as sns
# import numpy as np
# import scipy.stats as stats
# import matplotlib.pyplot as plt
import gastrodon as gd
from rdflib import *


def depthCounter(*args):
    g = Graph()
    g.parse('/Users/alessandro/Documents/PhD/WDOntology_100k_modified.owl')
    # g.parse('/home/ap1a14/WDOntology_100k_modified.owl')
    print('ontology parsed')

    e = gd.LocalEndpoint(g)

    e.update('''
        DELETE { ?Z rdfs:subPropertyOf ?A . } 
        WHERE { ?Z a owl:DatatypeProperty . ?A a owl:ObjectProperty .  }
    ''')

    e.update('''
        DELETE { ?Z a owl:Class . } where {?Z a owl:Class .  
        { ?Z rdf:type <http://www.wikidata.org/entity/Q11424> . } UNION
        { ?Z rdf:type <http://www.wikidata.org/entity/Q482994> . } UNION
        { ?Z rdf:type <http://www.wikidata.org/entity/Q5> . } UNION 
        {?Z a  <http://www.wikidata.org/entity/Q3305213> . } UNION 
        {?Z a <http://www.wikidata.org/entity/Q17152495> .} UNION 
        { ?Z a <http://www.wikidata.org/entity/Q15727816> .} UNION
        {?Z a owl:Class . ?Z rdf:type <http://www.wikidata.org/entity/Q4167410> .} UNION
        { ?Z a owl:Class . ?Z rdf:type <http://www.wikidata.org/entity/Q13406463> . } UNION
        { ?Z a owl:Class . ?Z rdf:type <http://www.wikidata.org/entity/Q14204246> . } UNION
        { ?Z a owl:Class . ?Z rdf:type <http://www.wikidata.org/entity/Q3918> . } 
    }
    ''')

    e.update('''
    DELETE {?Z a owl:Class .} 
    WHERE {?s a owl:Class . ?s a ?o . ?o rdfs:subClassOf+  <http://www.wikidata.org/entity/Q43229>. 
    FILTER(NOT EXISTS{?s rdfs:subClassOf ?c .}) }
    ''')

    e.update('''
        DELETE {?P a owl:AsymmetricProperty .} 
        WHERE { ?P a owl:TransitiveProperty . ?P a owl:AsymmetricProperty . }
    ''')

    e.update('''
        DELETE {?Z a owl:Class .} 
        where { ?Z rdf:type ?A . ?A rdfs:subClassOf+  <http://www.wikidata.org/entity/Q56061> . }
    ''')

    e.update('''
    DELETE {?Z rdf:type <http://www.wikidata.org/entity/Q502895> . } 
    where { ?Z rdf:type <http://www.wikidata.org/entity/Q502895> . ?Z rdfs:subClassOf+   <http://www.wikidata.org/entity/Q7239>.}
    ''')

    properties=e.select("""
       select ?class (count(?mid)-1 as ?depth) {
     {
       select ?root {
         ?root a owl:Class
         filter not exists {
           ?root rdfs:subClassOf ?superroot 
           filter ( ?root != ?superroot )
         }
       }
     }
    
     ?class rdfs:subClassOf* ?mid .
     ?mid rdfs:subClassOf* ?root .
    }
    group by ?class
    order by ?depth
    """)

    properties.to_csv("WDOntoDepth.csv")
    print('done!')


def main():
    depthCounter()

if __name__ == "__main__":
    main()