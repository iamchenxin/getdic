__author__ = 'z9764'
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import sys

def test1():
    r = requests.get("http://www.oxforddictionaries.com/us/definition/american_english/appreciate")
    soup = BeautifulSoup(r.text)
    enheader=0
    for header in soup.find_all("header"):
        print(header["class"])
        for cls in header['class']:
            if cls=="entryHeader":
                enheader=header
    if enheader==0:
        print("not find")
        return
    tmp=0;
    for div in enheader.find_all(class_="headsyllabified"):
        print("\n\n")
        print(div)
        print("\n\n")
    for div in enheader.find_all("div",class_="headpron"):
        print(div)

def GetMp3(xurl):
    r=requests.get(xurl)
    print(r.headers)
    print("\n")
    print(len(r.content))
    print(r.status_code)
    print(r.elapsed)

    if not r.ok:
        print("\n NOT OK \n")
        return


    with open("./mp3/test.mp3","wb") as mp3:
        size=0
        for block in r.iter_content(1024):
            if not block:
                print("finish")
                break;
            mp3.write(block)
            print(str(size)+"k")
            size+=1

def ReadTest(name):
    with open(name,"r") as file:
        count =0
        for line in file:
            print(line)
            count+=1
            if count>100:
                break

def PathTest():
    mypath = Path(".")
    for ps in mypath.iterdir():
        print(ps)
        if ps.is_dir():
            print("sub dir:")
            for pps in ps.iterdir():
                print("   "+ str(pps))
def MkPath():
    basepath = Path(".")
    mypath=basepath.joinpath("mp3")
    exct=0
    dspath=None
    while True:
        try:
            mypath.mkdir()
            print("成功创建{0}".format(mypath))
            break
        except FileExistsError as err:
            print("I/O error: {0}".format(err))
            mypath=basepath.joinpath("mp3"+str(exct))
            exct=exct+1

def FileTest():
    try:
        f=open("abc")
    except IOError as err:
        print("IOError err={0}".format(str(err)))
        print(sys.exc_info())
    except FileNotFoundError as err:
        print("FileNotFoundError,err={0}".format(str(err)))
    except:
        print("some other except")
        raise


class CCTmp:
    class CCCt:
        a=1
        b="asdasd"
    class CCCa:
        x="haha"
        b=666
    m1=CCCt()
    m2=CCCa()








#GetMp3("http://www.oxforddictionaries.com/us/media/american_english/us_pron/a/ame/ameri/american_dream_1_us_1.mp3")
#ReadTest(r"L:\soft\12dicts-5.0\3esl.txt")
#MkPath()
#FileTest()
ts=CCTmp()
print(str(ts))