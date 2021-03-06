# multiproc_test.py

import random
import multiprocessing
import subprocess
import os
import sys


def javaRun(jarFile, wdClasses, typeFile, fileName, fileOut):
    subprocess.call(['java', '-Xmx4280M', '-jar', jarFile, wdClasses, typeFile, fileName, fileOut])


if __name__ == "__main__":
    # procs = 4   # Number of processes to create

    # Create a list of jobs and then iterate through
    # the number of processes appending each process to
    # the job list
    jobs = []
    folder = sys.argv[1]
    jarFile = sys.argv[2]
    wdClasses = sys.argv[3]
    typeFile = sys.argv[4]
    fileOut = sys.argv[5]
    dirName = os.path.abspath(folder)

    for filename in os.listdir(folder):
        fileCsv = dirName + '/' + filename
        print(fileCsv)
        process = multiprocessing.Process(target=javaRun, args=(jarFile, wdClasses, typeFile, fileCsv, fileOut))
        jobs.append(process)

    # Start the processes (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")