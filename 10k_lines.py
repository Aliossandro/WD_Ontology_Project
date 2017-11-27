# -*- coding: utf-8 -*-
import os
import sys
import re


# import urllib3
# import threading
# import os
import bz2
# import datetime

def file_extractor(file_name):

    counter = 0


    with bz2.open(file_name, 'rt') as inputfile:
        with open('15k_items.xml') as f:
            for line in inputfile:
                f.write(line)
                f.write('\n')

                if '</page>' in line:
                    counter += 1

                if counter == 15000:
                    break


def main():
    file_extractor(sys.argv[1])


if __name__ == "__main__":
    main()