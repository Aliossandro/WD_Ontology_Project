#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson
import re
import bz2
import os
import sys
import pandas as pd
import urllib.parse
import csv
import seaborn as sns
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

class classAnalyser(object):

    def __init__(self, fileIn):
        self.fileIn = fileIn
        self.instanceCount()
        self.subclassCount()

    def instanceCount(self):
        statCount = pd.read_csv(self.fileIn, header=0)
        statCount = statCount[statCount['statproperty'] == 'P31']
        instanceCount = statCount.groupby('statvalue').nunique()['statementid']
        instanceCount = instanceCount.reset_index()
        self.fileWriter(instanceCount, 'instanceCount.csv')

    def subclassCount(self):
        statCount = pd.read_csv(self.fileIn, header=0)
        statCount = statCount[statCount['statproperty'] == 'P279']
        sclassCount = statCount.groupby('statvalue').nunique()['statementid']
        sclassCount = sclassCount.reset_index()
        self.fileWriter(sclassCount, 'subclassCount.csv')

    def fileWriter(self, df, fileOut):
        df.to_csv(fileOut, index=False)


# h.sort()
# hmean = np.mean(h)
# hstd = np.std(h)
# pdf = stats.norm.pdf(h, hmean, hstd)
# plt.plot(h, pdf)
# sns.distplot(h)
# h = np.array(h)
# sns.kdeplot(h, shade=True);


def main():
    file_name = sys.argv[1]
    classAnalyser(file_name)

if __name__ == "__main__":
    main()