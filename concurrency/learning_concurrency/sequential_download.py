
""" Sequential download """
# Concurrent image download
# one of the best use cases for multithreading due to the blocking nature of I/O
import urllib.request

def downloadImage(imagePath, fileName):
    print("Downloading Image from ", imagePath)
    urllib.request.urlretrieve(imagePath, fileName)

def main_seqential():
    for i in range(10):
        imageName = "temp/image-" + str(i) + ".jpg"
        downloadImage("http://lorempixel.com/400/200/sports", imageName)




""" Concurrent download """
import threading
import time

def executeThread(i):
    imageName = "temp/image-" + str(i) + ".jpg"
    downloadImage("http://lorempixel.com/400/200/sports", imageName)

def main_concurrent():
    t0 = time.time()
    # create an array which will store a reference to all of our threads
    threads = []
    for i in range(10):
        thread = theading.Thread(target=executeThread, args=(i,))
        threads.append(thread)
        thread.start()

    # ensure that all the threads in our array have completed their execution
    # before we log the total time to complete
    for i in threads:
        i.join()

    t1 = time.time()
    totalTime = t1 - t0
    print("Total Execution Time {}".format(totalTime))



if __name__ == "__main__":
    main_seqential()
    main_concurrent()
