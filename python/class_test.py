class Test:
    def __init__(self, num):
        self.num = num  # このクラスが持つ「num」変数に引数を格納

    def print_num(self):
        print('引数で渡された数字は{}です。'.format(self.num))


test = Test(10)  # ここで渡された引数が__init__のnumに渡される
test.print_num()
