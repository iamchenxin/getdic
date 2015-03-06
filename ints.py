__author__ = 'z9764'

import threading
import time
import random

status =True



def init_file(filename):
    global file
    try:
        file=open(filename,"r")
    except Exception as err:
        print("check file {0} exist?".format(filename))
        raise

file=None
word_free=True
class mywork(threading.Thread):

    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name

    def run(self):
        print("i am {0},i am in work".format(self.name))

        while True:
            second=random.random()
            second=second*5
            print("{0}Read-{1}- ".format(self.name,self.getword()))
#            print(" {0} sleep {1} ".format(self.name,second))
            time.sleep(second)
            if status!=True:
                break

        print("i am quit,{0}".format(self.name))

    def getword(self):
        global file
        global word_free
        while True:
            if word_free==True:
                word_free=False
                rt = file.readline()
                word_free=True
                return rt
            else:
                print("{0} blocked by getword")



count = 0
init_file("3esl.txt")

while count<20:
    count=count+1
    aa=input(r"---->")
    if aa == "q":
        print("press 'q' ")
        status=False
    else:
        worker=mywork(aa)
        worker.start()

