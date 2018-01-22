# multiproc_test.py

import random
import multiprocessing
import subprocess
import os
import sys


def javaRun(fileName):
    subprocess.call(['java', '-Xmx4280M', '-jar', '/Users/alessandro/Downloads/ExplaAll.jar', '/Users/alessandro/Documents/PhD/WDOnto_classes.owl', '/Users/alessandro/Documents/PhD/WDSignedtriples-types.owl', fileName, '/Users/alessandro/Documents/PhD/WDNewExpl.txt'])


# def list_append(count, id, out_list):
# 	"""
# 	Creates an empty list and then appends a
# 	random number to the list 'count' number
# 	of times. A CPU-heavy operation!
# 	"""
# 	for i in range(count):
# 		out_list.append(random.random())

if __name__ == "__main__":
    procs = 4   # Number of processes to create

    # Create a list of jobs and then iterate through
    # the number of processes appending each process to
    # the job list
    jobs = []
    folder = sys.argv[1]
    dirName = os.path.abspath(folder)

    for filename in os.listdir(folder):
        fileCsv = dirName + '/' + filename
        print(fileCsv)
        process = multiprocessing.Process(target=javaRun, args=(fileCsv,))
        jobs.append(process)

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")