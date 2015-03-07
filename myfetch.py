__author__ = 'z9764'
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import sys
import re
import json
import threading
import time




mpKeyAbbreviation={"name":"name","rank":"rank","syl":"syllabification","lin":"linebreaks","pro":"pronunciation","voi":"voice","definition":"definition","meaning":"meaning","example":"example","noun":"noun",
                  "verb":"verb","ori":"origin","phr":"phrase","deri":"derivative","rhy":"rhyme","see":"seealso","near":"nearby"}

###mpDefinition={[{"partOfSpeech":None,"inflection":None,"sense":None },],}
mpDicSenseData={"meaning":None,"example":None,"synonyms":None,"subsense":None}    #{"meaning":None,"example":["ERROR",],"synonyms":["ERROR",],"subsense":[]}
mpDicData = {"word": {"name": None, "rank": None, "syl": None,"lin":None, "pro":None},
            "definition":None,#{[{"partOfSpeech":None,"inflection":None,"sense":None },]},   #all of this item are mpDicDefData[]
            "Origin":None,"Usage":None,
            "Phrases":None,"Phrasal verbs":None, "Derivatives":None, "rhyme":None, "See":None, "Nearby":None} #

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

class FecWordEnd(FecError):
    pass
class FecUnfindWord(FecError):
    def __init__(self,word):
        self.word=word
    pass

def find_all_mustbe(beati, name=None, attrs={}, recursive=True, text=None,
             limit=None, **kwargs):
    rt = beati.find_all(name,attrs,recursive,text,limit,**kwargs)
    if not rt:
        raise FecMissSyntaxErr("name={0},attrs={1}".format(name,attrs))
    return rt

def find_mustbe(beati, name=None, attrs={}, recursive=True, text=None,
         **kwargs):

    rt = beati.find(name,attrs,recursive,text,**kwargs)
    if not rt:
        print(beati.prettify())
        raise FecMissSyntaxErr("name={0},attrs={1}".format(name,attrs))
    return rt



class CDicFetch:
    mDicUrl = None
    save_fold = None
    def __init__(self,savefold,DicUrl):  # at now just store per word per file
        try:
            tmppath = Path(".").joinpath(savefold)
            if(tmppath.is_dir()==False):
                tmppath.mkdir()
            self.save_fold=tmppath
            self.mDicUrl= DicUrl
            self.name="000"
            FecError.save_fold=self.save_fold
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



    def down_file(self,url,savename):
        r_file=None
        the_file=None

        try:
            r_file=requests.get(url)
            the_file=open(str(self.save_fold.joinpath(savename)),"wb")
        except Exception as err:
            print("mp3 write err",err)
            raise
        else:
            file_rsize=0
#            print("Begin Download {0}".format(savename))
            for block in r_file.iter_content(1024):
                if not block:
                    break
                the_file.write(block)
                print(".",end="")
                file_rsize+=1
            print("Down,{0}K".format(file_rsize))
        finally:
            the_file.close()

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
#            print(subdefinition["partOfSpeech"])
            se2_list=[]
            se2_list=means.find_all("div",class_="se2")
            if se2_list.__len__()<1:
                se2_list=[means,]
            for webse2 in se2_list:
                main_se2 = {"meaning":None,"example":None,"synonyms":None,"subsense":None}
                webmain_se2 = find_mustbe(webse2,"div",class_="msDict sense")
                main_se2 = self.get_def(webmain_se2)
                main_se2["subsense"]=[]
                for websub_s in webse2.find_all("div",class_="msDict subsense"):
                    main_se2["subsense"].append( self.get_def(websub_s) )
                subdefinition["sense"].append(main_se2)
            defss.append(subdefinition)
        return defss

    def get_header(self,webheader,dstUrl,store_word,worker_name):
        lWord={}
        global loggg

        webName=webheader.find(class_="pageTitle")

        lWord["name"]=webName.get_text()
        rankstr=webName.next_sibling["class"][0]
        rankrt= re.findall(r"^top[0-9]{1,5}",rankstr)
        if rankrt:
            lWord["rank"]=rankrt[0]
        webSyl=webheader.find(class_="syllabified")
        if webSyl!=None:
            lWord["syl"]=webSyl.string.strip()
        webLin=webheader.find(class_="linebreaks")
        if webLin!=None:
            lWord["lin"]=webLin.string.strip()
        webPro=webheader.find(class_="headpron")
        if webPro==None:
            webPro=find_mustbe(webheader.parent,"div",class_="headpron")
        if webPro!=None:
            prore=re.compile(r"/.*?/")
            pro_rt=prore.findall(webPro.get_text())
            if pro_rt:
                lWord["pro"]=pro_rt[0]

        rrmp3 = webPro.div["data-src-mp3"]
        rrogg = webPro.div["data-src-ogg"]

        if rrmp3:
            print("{0} begin download {1}".format(worker_name,store_word+".mp3"),end="")
            self.down_file(rrmp3,store_word+".mp3")
        else:
            print("NO!MP3!at URL::{0}".format(dstUrl))
            loggg["noMp3"].append(store_word)
        if rrogg:
            print("{0} begin download {1}".format(worker_name,store_word+".ogg"),end="")
            self.down_file(rrogg,store_word+".ogg")
        else:
            print("NO!OGG!at URL::{0}".format(dstUrl))
            loggg["noOgg"].append(store_word)
        return lWord



#### the main definition may be multipul,like "go" ,now just read one,fix it later
    def ExtractPage(self,word,worker_name):
        word=word.strip()
        pp=re.compile(r"[^a-zA-z]")
        store_word=pp.sub("_",word)
        dstUrl=self.mDicUrl+word
        data=dict(mpDicData)
        FecError.dstUrl=dstUrl
        FecError.word=word

        try:
            r=requests.get(dstUrl,timeout=(6.1,39))
            if r.status_code==404:
                raise FecUnfindWord(word)
        except Exception as err:
            print("unknown error:{0},sys info is{1}".format(err,sys.exc_info()))
            raise
        else:
            print("{0} open {1}".format(worker_name,dstUrl))
        soup =BeautifulSoup(r.text)

        contentup = soup.find("div",id="firstClickFreeAllowed")
        contentss = find_all_mustbe(contentup,"div",class_="entryPageContent")
        if contentss.__len__()<0:
            raise FecMissSyntaxErr(entryPageContent)
        content=contentss[0]

        # get word inf and main definitions
        webheader = find_mustbe(content,"header",class_="entryHeader")
        data["word"]=self.get_header(webheader,dstUrl,store_word,worker_name)

        webdefs_must=find_all_mustbe(content,"section",class_="se1 senseGroup")
        data["definition"]=self.get_main_content(content)

        #process word's homograph
        content_plus = contentss[1:]
        data["homograph"]=[]
        for webhomograph in content_plus:
            homo_word={"word":[],"definition":[]}
            webheader_s=find_mustbe(webhomograph,"header",class_="entryHeader")
            homo_word["word"]=self.get_header(webheader_s,dstUrl,store_word,worker_name)
            webdefs_must_s=find_all_mustbe(webhomograph,"section",class_="se1 senseGroup")
            homo_word["definition"]=self.get_main_content(webhomograph)
            data["homograph"].append(homo_word)

        # etymology  <section class="etymology">
        for etymology in content.find_all("section",class_="etymology"):
            tmph3=find_mustbe(etymology,"h3")
            ety_str =tmph3.get_text()
            tmph3.decompose()
            if re.search(r"\brhyme\b",ety_str):
                data["rhyme"]=etymology.get_text()
            else:
                data[ety_str]=etymology.get_text()
        # phrases & phrase verb  <section class="subEntryBlock phrasesSubEntryBlock"><h3>Phrasal verbs</h3>
        for phrases in content.find_all("section",class_="phrasesSubEntryBlock"):
            phr = find_mustbe(phrases,"h3").string
            thedl = find_mustbe(phrases,"dl")
            data[phr]=[]

            for webphr_def in find_all_mustbe(thedl,"div",class_="subEntry"):
                phr_def={}
                wordss=find_mustbe(find_mustbe(webphr_def,"dt") ,"h4").get_text()
                phr_def["words"]=wordss
                tmpdef = webphr_def.find("dd",class_="sense")
                definition=None

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

#  read div responsive_cell_right,nearby and see also
        related = soup.find("div",class_="responsive_cell_right").find("div",class_="relatedBlock")
        if related:
            title = related.find("h4")
            if title:
                re_con = title.find_next_sibling("div",class_="responsive_columns_2_on_desktop")
                if re_con:
                    for ron_word in re_con.find_all("span",class_="alpha_title"):
                        title_str=re.findall(r"[a-zA-Z]+\b",title.string)[0]
                        data[title_str]=[]
                        data[title_str].append(ron_word.get_text())
                    title2=re_con.find_next_sibling("h4")
                    if title2:
                        re_con2 = title2.find_next_sibling("div",class_="responsive_columns_2_on_desktop")
                        if re_con2:
                            title2_str=re.findall(r"[a-zA-Z]+\b",title2.string)[0]
                            data[title2_str]=[]
                            for rcon2_word in re_con2.find_all("span",class_="arl4"):
                                data[title2_str].append(rcon2_word.get_text())


                        ## store to json
        jsonname=store_word+".json"
        with open(str(self.save_fold.joinpath(jsonname)),"w") as file_j:
            out_str=json.dumps(data)
            file_j.write(out_str)
        print("{0} FINISH {1}.json".format(worker_name,store_word))



def init_wordfile(filename):
    global word_file
    try:
        word_file=open(filename,"r")
    except Exception as err:
        print("Read word's file error,please check the file '{0}' exist".format(filename))
        raise
word_free=True
word_file=None
block_count=0;
def fget_word():
    global word_free
    global word_file
    global block_count
    while True:
        if word_free==True:
            word_free=False
            try:
                str=word_file.readline()
            except Exception as err:
                print(err)
                print("no word supply")
                raise FecWordEnd()
            word_free=True
            if str:
                loggg["word_count"] = loggg["word_count"]+1
                loggg["current_word"]=str
                return str
        else:
            block_count=block_count+1
            print("WORD READ BLOCKED~~~~~")
            if block_count>50:
                raise FecWordEnd()

def close_wordfile():
    word_file.close()




loggg={"word_count":0,"worker_table":{}, "current_word":None,"syntax_wrong":[],"badword_list":[],"unfind_word":[], "noMp3":[],"noOgg":[]}

def log_Badword(word):
    global badword_list
    badword_list.append(word)

def log_store():
    global loggg
    with open("diclog.json","w") as logfile:
        logfile.write( json.dumps(loggg))

def convert_word(word):
    word=word.strip()
    word=re.sub(r"\s+","-",word)
    return word

q_status=False
class fetchWorker(threading.Thread):
    def __init__(self,outfold,fget_word,dsturl,name="anony"):
        threading.Thread.__init__(self)
        self.outfold=outfold
        self.fget_word=fget_word
        self.dsturl=dsturl
        self.name=name
        self.dicfetch=CDicFetch(outfold,dsturl)
        self.retry_word=None
        self.worker_count=0


    def run(self):
        global loggg
        global q_status
        print("{0} run.run.run.".format(self.name))
        word=None
        while q_status==False:
            try:
                if self.retry_word!=None:
                    self.dicfetch.ExtractPage(self.retry_word,self.name)
                    print("{0} retry [{1}] success".format(self.name,self.retry_word))
                    self.retry_word=None  # if process it ,set to None
                else:
                    word=self.fget_word()
                    if word:
                        word=convert_word(word)
                        self.worker_count=loggg["word_count"]
                        print("{0} read word [{1}]".format(self.name,word))
                        self.dicfetch.ExtractPage(word,self.name)
            except requests.Timeout as timeout:
                print(timeout)
                print("{0} time out ->{1},try again".format(self.name, word))
                self.retry_word=word
                continue
            except FecMissSyntaxErr as err:
                print(err)
                print("{0} can't analyze syntax at [{1}] ".format(self.name,word))
                loggg["syntax_wrong"].append(word)
                continue
            except FecUnfindWord as err:
                print("{0} unfind [{1}] in web,move to next word".format(self.name,word))
                loggg["unfind_word"].append(word)
                continue
            except FecWordEnd as err:
                print("FecWordEnd")
                break
            except Exception as err:
                loggg["badword_list"].append(word)
                print(str(err))
                print("!!!{0} can not read [{1}],but still read next word".format(self.name,word))
                continue
            else:
                pass
            finally:
                pass
        print("{0} is end!!!".format(self.name))


def mainloop(outfold,dict,url):
    worker_list=[]
    init_wordfile(dict)
    global q_status
    try:
        while True:
            keyin =input()
            if keyin =="q":
                q_status=True
                keyin=None
            if keyin =="ex":
                q_status=True
                time.sleep(10)
                keyin=None
                break
            if keyin =="s":
                workerdd={}
                for ww in worker_list:
                    workerdd[ww.name]=ww.worker_count
                loggg["worker_table"]=workerdd
                log_store()
                keyin=None
            if keyin!=None:
                worker=fetchWorker(outfold,fget_word,url,keyin)
                worker_list.append(worker)
                worker.start()
    except Exception as err:
        log_store()
        print(err)
        raise
    finally:
        close_wordfile()



# sys.argv[1] = out put fold ,sys.argv[2]= dictionary, sys.argv[3] = dst url
if __name__ == '__main__':
    mainloop(sys.argv[1],sys.argv[2],sys.argv[3])
