__author__ = 'z9764'


class CDicData:
    class WORD:
        name=None
        rank=None
        syllabification=None
        pronunciation=None
        voice=None
    class DEFINITION:
        text=None
        example=None
        synonyms=None

    class PHRASE:
        phrase_words=None
        explain=None
        example=None
        synonyms=None

    word=WORD()
    definition={}.fromkeys(("noun","verb"),None)
    origin=None  # just some text
    phrase=[]     #PHRASE lists
    derivative=[]  #string lists
    rhyme=[] #string list
    seealso=[] #string list
    nearby=[]  #string list
    pass

mpKeyAbbreviation={"name":"name","rank":"rank","syl":"syllabification","lin":"linebreaks","pro":"pronunciation","voi":"voice","def":"definition","mea":"meaning","exa":"example","noun":"noun",
                  "verb":"verb","ori":"origin","phr":"phrase","deri":"derivative","rhy":"rhyme","see":"seealso","near":"nearby"}

mDicDefData={"mea":None,"exa":[],"syno":[]}
mDicData = {"word": {"name": None, "rank": None, "syl": None, "pro":None},
            "def":{"noun":[],"verb":[]},
            "ori":None, "phr":[], "deri":[], "rhy":[], "see":[], "near":[]}

ma = dict(mDicData)
mb = dict(mDicData)
ma["ori"]="hahashash"
mb["phr"]=["nihao","123"]
#print(ma)
#print(mb)
#print(mDicData)

for k,v in mb.items():
    print("{0}={1}".format(mKeyAbbreviation[k],v))
#    print(mKeyAbbreviation[k])
#    print(v)