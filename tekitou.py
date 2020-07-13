import numpy as np

NATOM = 4
NCEL = 2
LCEL = 1.0
np.random.seed(seed=1)


class Test:
    def __init__(self):
        self.x = np.random.rand()

    def test_method(self, num):
        print(self.x)




test = []
for i in range(3):
    test = test + [Test()]
    test[i].test_method(i)
