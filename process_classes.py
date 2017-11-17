# -*- coding: utf-8 -*-
import os
import sys
import re
import pandas as pd

def writeClasslist(classList, file_name):
    ###write properties
    with open(file_name, 'w') as f:
        for ele in list(classList):
            f.write(ele + '\n')

        f.close()


dname = '/Users/alessandro/Documents/PhD/WD_ontology/'


###All subjects of P279
fname = dname+'classesP279_1611.txt'
with open(fname) as f:
    p279 = f.readlines()

p279 = [x.strip() for x in p279]

###All objects of P31
fname = dname+'classesP31_1611.txt'
with open(fname) as f:
    p31 = f.readlines()

p31 = [x.strip() for x in p31]

###All objects of P279
fname = dname+'superclasses_1611.txt'
with open(fname) as f:
    p279s = f.readlines()

p279s = [x.strip() for x in p279s]


###items with subclasses or instances
selItems = set(p279s).union(p31)

writeClasslist(selItems, 'classSelection.txt')
