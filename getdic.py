__author__ = 'z9764'
import myfetch



# str="http://www.oxforddictionaries.com/definition/english/"
#test = CDicFetch("test","http://www.oxforddictionaries.com/definition/american_english/")
#test.ExtractPage("go")

myfetch.init_wordfile("3esl.txt")
dicf=myfetch.CDicFetch("test","http://www.oxforddictionaries.com/definition/english/")
word = myfetch.convert_word("absentlya")
dicf.ExtractPage(word,"德华")

print( myfetch.loggg)