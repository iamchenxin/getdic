__author__ = 'z9764'
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import sys
import re




mpKeyAbbreviation={"name":"name","rank":"rank","syl":"syllabification","lin":"linebreaks","pro":"pronunciation","voi":"voice","definition":"definition","meaning":"meaning","example":"example","noun":"noun",
                  "verb":"verb","ori":"origin","phr":"phrase","deri":"derivative","rhy":"rhyme","see":"seealso","near":"nearby"}

###mpDefinition={[{"partOfSpeech":None,"inflection":None,"sense":None },],}
mpDicSenseData={"meaning":None,"example":None,"synonyms":None,"subsense":None}    #{"meaning":None,"example":["ERROR",],"synonyms":["ERROR",],"subsense":[]}
mpDicData = {"word": {"name": None, "rank": None, "syl": None,"lin":None, "pro":None},
            "definition":None,#{[{"partOfSpeech":None,"inflection":None,"sense":None },]},   #all of this item are mpDicDefData[]
            "Origin":None,"Usage":None,
            "Phrases":["ERROR",],"Phrasal verbs":[], "deri":["ERROR",], "rhyme":["ERROR",], "see":["ERROR",], "near":["ERROR",]} #

class FecError(Exception):
    """Hello,i am error from CDicFetch~~
    Attributes:
    define in class CDicFetch
    __init__()
            FecError.mMp3Fold=self.mMp3Fold
            FecError.mDicUrl=self.mDicUrl
    ExtractPage(self,word):
        FecError.dstUrl=dstUrl
        FecError.word=word
    """
    pass

class FecMissSyntaxErr(FecError):
    """the error is raised,cause designing bugs,i do a false anology at this syntax !so amend it !
    Attributes:

    """
    def __init__(self,syntax):
        self.syntax=syntax

def find_all_mustbe(beati, name=None, attrs={}, recursive=True, text=None,
             limit=None, **kwargs):
    rt = beati.find_all(name,attrs,recursive,text,limit,**kwargs)
    if not rt:
        raise FileExistsError("name={0},attrs={1}".format(name,attrs))
    return rt

def find_mustbe(beati, name=None, attrs={}, recursive=True, text=None,
         **kwargs):
    print("iam in find_mustbe")
    rt = beati.find(name,attrs,recursive,text,**kwargs)
    if not rt:
        print(beati.prettify())
        raise FileExistsError("name={0},attrs={1}".format(name,attrs))
    return rt



class CDicFetch:
    mWordsIO = None
    mDicUrl = None
    mMp3Fold = None
    mOxurl="http://www.oxforddictionaries.com/definition/american_english/"
    def __init__(self,MpsFold,WordsFileName,DicUrl):
        try:
            tmppath = Path(".").joinpath(MpsFold)
            if(tmppath.is_dir()==False):
                tmppath.mkdir()
            self.mMp3Fold=tmppath
            self.mWordsIO = open(WordsFileName,"r")
            self.mDicUrl= DicUrl
            FecError.mMp3Fold=self.mMp3Fold
            FecError.mDicUrl=self.mDicUrl
        except FileExistsError as err:
            print("FileExistsError,err={0}\n should check the fold!same name file".format(str(err)))
            raise
        except FileNotFoundError as err:
            print("FileNotFoundError,err={0} there is no file ".format(str(err)))
            raise
        except IOError as err:
            print("I/O error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            print("fold and words are ready!")
        finally:

            pass



    def downmp3(self,url,mp3name):
        rmp3=None
        mp3_file=None

        try:
            rmp3=requests.get(url)
            mp3name=mp3name+".mp3"
            mp3_file=open(str(self.mMp3Fold.joinpath(mp3name)),"wb")
        except Exception as err:
            print("mp3 write err",err)
            raise
        else:
            mp3_rsize=0
            print("Begin Download {0}".format(mp3name))
            for block in rmp3.iter_content(1024):
                if not block:
                    break
                mp3_file.write(block)
                print(".",end="")
                mp3_rsize+=1
            print("Down,{0}K".format(mp3_rsize))
        finally:
            mp3_file.close()

    def get_def(self,webdef_s):
        def_section ={}
        def_section["example"]=[]
        meaning = webdef_s.find("span",class_="definition")
        if meaning:
            def_section["meaning"]=meaning.get_text()
        for exa in webdef_s.find_all("span",class_="exampleGroup"):
            def_section["example"].append(exa.get_text())
        for exa in webdef_s.find_all("li",class_="sentence"):
            def_section["example"].append(exa.get_text())
        Synonyms = webdef_s.find("div",class_="entrySynList")
        if Synonyms!=None:
            def_section["synonyms"]=Synonyms.get_text()
        return def_section

    def get_all_def(self,content):
        dicdef=dict()
        sections = content.find_all("section",class_="se1 senseGroup")
        for sec in sections:  #defenition
        #    print(sec.prettify())
            partOfSpeech = sec.h3.get_text().strip()
            dicdef[partOfSpeech]=[]
            dicdef[partOfSpeech].append((self.get_def(sec.find("div",class_="msDict sense")) ))

            for subdef in sec.find_all("div",class_="msDict subsense"):
                dicdef[partOfSpeech].append((self.get_def(subdef) ))
        return dicdef

# coresspending to <div class="entryPageContent">,it contains the main explains of the word,but can have more than one main content
    def get_main_content(self,content):
        defss=[]
        for means in content.find_all("section",class_="se1 senseGroup"):
            subdefinition = dict()

            subdefinition["partOfSpeech"]=find_mustbe(means,class_="partOfSpeech").string
            inflectionGroup=means.find(class_="inflectionGroup")
            if inflectionGroup:
                subdefinition["inflectionGroup"] =inflectionGroup.get_text()
            subdefinition["sense"]=[]
            for webse2 in find_all_mustbe(means,"div",class_="se2"):
                main_se2 = {"meaning":None,"example":None,"synonyms":None,"subsense":None}
                webmain_se2 = find_mustbe(webse2,"div",class_="msDict sense")
                main_se2 = self.get_def(webmain_se2)
                main_se2["subsense"]=[]
                for websub_s in webse2.find_all("div",class_="msDict subsense"):
                    main_se2["subsense"].append( self.get_def(websub_s) )
                subdefinition["sense"].append(main_se2)
            defss.append(subdefinition)
        return defss





    def ExtractPage(self,word):

        dstUrl=self.mDicUrl+word.strip()
        data=dict(mpDicData)
        FecError.dstUrl=dstUrl
        FecError.word=word

        try:
            r=requests.get(dstUrl)
        except Exception as err:
            print("unknown error:{0},sys info is{1}".format(err,sys.exc_info()))
            raise
        except:
            print("they said Exception is all??",sys.exc_info())
            raise
        else:
            print("successful open URL| {0}".format(dstUrl))
        soup =BeautifulSoup(r.text)
        contentup = soup.find("div",id="firstClickFreeAllowed")
        content = contentup.find("div",class_="entryPageContent")
#        header = content.find("div",class_="entryHeader")
#        content = soup.select("#firstClickFreeAllowed .entryPageContent")[0]
        lWord=data["word"]
        header = content.find("header",class_="entryHeader")
        webName=header.find("strong")
        lWord["name"]=webName.string
        lWord["rank"]=webName.next_sibling["class"][0]
        webSyl=header.find(class_="syllabified")
        if webSyl!=None:
            lWord["syl"]=webSyl.string
        webLin=header.find(class_="linebreaks")
        if webLin!=None:
            lWord["lin"]=webLin.string
        webPro=header.find(class_="headpron")
        lWord["pro"]=webPro.get_text()
        print(webPro.div["data-src-mp3"])

        self.downmp3(webPro.div["data-src-mp3"],word.strip())
        webdefs_must=find_all_mustbe(content,"section",class_="se1 senseGroup")

        for mydef in webdefs_must:
            print("....")
            print(mydef.find(class_="partOfSpeech").string)
        data["definition"]=self.get_main_content(content)

        # etymology  <section class="etymology">
        for etymology in content.find_all("section",class_="etymology"):
            tmph3=find_mustbe(etymology,"h3")
            str =tmph3.get_text()
            tmph3.decompose()
            if re.search("\brhyme\b",str):
                data["rhyme"]=etymology.get_text()
            else:
                data[str]=etymology.get_text()
        # phrases & phrase verb  <section class="subEntryBlock phrasesSubEntryBlock"><h3>Phrasal verbs</h3>
        for phrases in content.find_all("section",class_="phrasesSubEntryBlock"):
            phr = find_mustbe(phrases,"h3").string
            thedl = find_mustbe(phrases,"dl")
            data[phr]=[]
            print(phr)
            for webphr_def in find_all_mustbe(thedl,"div",class_="subEntry"):
                phr_def={}
                wordss=find_mustbe(find_mustbe(webphr_def,"dt") ,"h4").get_text()
                phr_def["words"]=wordss
                tmpdef = webphr_def.find("dd",class_="sense")
                definition=None
                print(wordss)
                if tmpdef:
                    definition=self.get_def(tmpdef)
                else:
                    tmpdef = webphr_def.find_all("div",class_="se2")
                    if tmpdef:
                        definition=[]
                        for sub_def in tmpdef:
                            definition.append(self.get_def(sub_def))
                phr_def["definition"]=definition

                data[phr].append(phr_def)

        print(data["definition"][0])
        print(data["definition"][1])

test = CDicFetch("test","3esl.txt","http://www.oxforddictionaries.com/definition/american_english/")
test.ExtractPage("practice")
