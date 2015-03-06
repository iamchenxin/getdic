__author__ = 'z9764'
import myfetch

def mainloop():
    worker_list=[]
    init_wordfile("3esl.txt")
#    worker=fetchWorker("mydic",fget_word,"http://www.oxforddictionaries.com/definition/american_english/","德华")
#    worker.start()
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
                log_store()
                keyin=None
            if keyin!=None
                worker=fetchWorker("mydic",fget_word,"http://www.oxforddictionaries.com/definition/american_english/",keyin)
                worker_list.append(worker)
                worker.start()
    except Exception as err:
        log_store()
        print(err)
        raise
    finally:
        close_wordfile()


#test = CDicFetch("test","http://www.oxforddictionaries.com/definition/american_english/")
#test.ExtractPage("go")

if __name__ == '__main__':
    mainloop()
