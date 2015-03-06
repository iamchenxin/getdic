__author__ = 'z9764'
import re

str = "Words that rhym1ewith fire"

aa=re.search(r"\brhyme\b",str)
bb=re.search(r"rhyme",str)
print(aa)
print(bb)


str2 = "Words that rhym1ewith fire"
pp=re.compile(r"[^a-zA-z]")
print(pp.sub("_",str2))

str3=r"top1000n1unciation:  /ˈfī(ə)r/ "

p3=re.compile(r"/.*?/")
b3=p3.findall(str3)
print(b3)
print(b3[0])

p4=re.compile(r"^top[0-9]{1,5}")
b4=p4.findall(str3)
print(b4)

str4="11  Words that rhym1ewith"
b5=re.findall(r"[a-zA-Z]+\b",str4)
print(b5)

mylist=[]
str5 ="accommodations\n"
mylist.append(str5)
str5=str5.strip()
mylist.append(str5)
print(str5)

str6="abbr.\n"
str6=str6.strip()
mylist.append(str6)
print(str6)

print(mylist)
