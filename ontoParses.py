#!/usr/bin/python
# -*- coding: utf-8 -*-

###fix & and <> in descriptions
### collectionof and rdf:Class about instead of resource

import ujson
import re
import bz2
import os
import fileWriter
from lxml import etree

