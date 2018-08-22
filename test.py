


num = 0
class t(object):
    def __init__(self):
        print('init')
    def run(self):
        global num
        num = num + 1
        print("哈哈%d" % (num))






if __name__ =='__main__':
    h = t()
    h.run()



