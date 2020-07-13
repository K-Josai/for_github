class Test:
    def __init__(self):
        self.x = None

    def test_method(self):
        self.x = 0.0
        print(self.x)


test = Test()
test.test_method()
