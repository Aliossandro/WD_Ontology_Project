import ujson
import re
import bz2
import os
import fileWriter

def guardafillo(file_name):
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

            matcho = re.match(r'\{\"type\"\:\"item\"\,\"id\"\:\"[Qq][0-9]{1,}', str(line))
            if not matcho:
                print(line[0:35])
            else:
                print(matcho.group(0))