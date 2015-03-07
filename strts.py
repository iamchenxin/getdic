__author__ = 'z9764'

mystr ="hehehe"



def get_str():
    global mystr
    return mystr

class Tsstr:
    def __init__(self):
        self.mystr=get_str()

    def ptstr(self):
        print(self.mystr)

ts1 = Tsstr()

mystr="liumang"

ts2=Tsstr()

mystr="xiaoming"

ts3=Tsstr()
mystr="huahua"
ts1.ptstr()
ts2.ptstr()
ts3.ptstr()

tdss=" "

if tdss:
    print("TDS True pass")

print(type(tdss))