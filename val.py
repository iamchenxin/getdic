__author__ = 'z9764'

class Cts:

    def test(self):
        val = "test!"
        print(val)
    def test_cts(self):

        print(self.val)

    def test_3(self):
        val="lv 1!"
        if True:
            val="lv 2"
            print(val)
        print(val)


def word_gen():
    count =0
    def get_word():
        nonlocal count
        count=count+1
        return "N{0}M".format(count)
    return get_word

Cts.val="out cts member"

cc=Cts()
cc.test()
cc.test_cts()
cc.test_3()

word = word_gen()
print(word())
print(word())
print(word())
print(word())
print(word())
print(word())
word_gen.count=66
print(word())
print(word())
