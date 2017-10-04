import ujson
import smart_open
import threading
import queue
import sys

QUEUE_SIZE = 100000
sentinel = object()

def extractClassesP31(line):
    classesP31 = []

    try:
        lineParsed = ujson.loads(line[:-2])

        if 'P31' in lineParsed['claims'].keys():
            for i in lineParsed['claims']['P31']:
                try:
                    superClass = i['mainsnak']['datavalue']['value']['id']
                    classesP31.append(superClass)
                except:
                    print(i)

    except:
        print(line)

    return classesP31


def extractClassesP279(line):
    classesList = []
    classesP31 = []

    try:
        lineParsed = ujson.loads(line[:-2])

        if 'P279' in lineParsed['claims'].keys():
            entityID = lineParsed['id']
            classesList.append(entityID)
            for i in lineParsed['claims']['P279']:
                try:
                    superClass = i['mainsnak']['datavalue']['value']['id']
                    classesList.append(superClass)
                except:
                    print(i)

    except:
        print(line)

    return classesList

def read_file(file_name, queueJob):
    for line in smart_open.smart_open(file_name):
        queueJob.put(line)
    print('100k read')
    queueJob.put(sentinel)


def process(inqueue, outqueue):
    for line in iter(inqueue.get, sentinel):
        outqueue.put(extractClassesP279(line))
    print('100k P279 done!')
    outqueue.put(sentinel)
    write_file('P279_classes.csv', outqueue)

def processP31(inqueue, outqueue):
    for line in iter(inqueue.get, sentinel):
        outqueue.put(extractClassesP31(line))
    print('100k P31 done!')
    outqueue.put(sentinel)
    write_file('P31_classes.csv', outqueue)


def write_file(name, queue):
    with open(name, "a") as f:
        for line in iter(queue.get, sentinel):
            print(line)
            f.write(line)

    # f = open(name, 'w')
    # s1 = '\n'.join(l1)
    # f.write(s1)
    # f.close()

def main():
    file_name = sys.argv[1]

    inq = queue.Queue(maxsize=QUEUE_SIZE)
    outq = queue.Queue(maxsize=QUEUE_SIZE)
    outq2 = queue.Queue(maxsize=QUEUE_SIZE)

    threading.Thread(target=read_file, args=(file_name, inq)).start()
    threading.Thread(target=process, args=(inq, outq)).start()
    threading.Thread(target=processP31, args=(inq, outq2)).start()


if __name__ == "__main__":
    main()