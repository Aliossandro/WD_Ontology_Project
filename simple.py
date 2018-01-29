# multiproc_test.py

import random
import multiprocessing
import subprocess
import os
import sys


# def javaRun(jarFile, wdClasses, typeFile, fileName, fileOut):
#     subprocess.call(['java', '-Xmx4280M', '-jar', jarFile, wdClasses, typeFile, fileName, fileOut])

def countSth(fileName):
    with open(fileName, 'r') as f:
        for i in xrange(1000000):
            f.write(i)
        f.close()


if __name__ == "__main__":
    # procs = 4   # Number of processes to create

    # Create a list of jobs and then iterate through
    # the number of processes appending each process to
    # the job list
    jobs = []
    folder = sys.argv[1]

    for num in xrange(16):
        process = multiprocessing.Process(target=countSth, args=(folder,))
        jobs.append(process)

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")
