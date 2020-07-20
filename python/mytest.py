from particle import Particle
from ensemble import Ensemble
from field import Field
import numpy as np

def ensemble_test():
    ATOM_NUM = 2

    paricles = [Particle() for i in range(ATOM_NUM)]

    ensemble = Ensemble(paricles)

    print("位置の配列\n", ensemble.positions)

    ensemble.positions += 1 #全体に+1
    print("+1\n", ensemble.positions)

    ensemble.positions *= 2 #全体に*2
    print("*2\n", ensemble.positions)

    ensemble.positions *= np.array([1, 2, 3]) #x*1, y*2, z*3
    print("x*1, y*2, z*3\n", ensemble.positions)

    ensemble.positions = np.ones((ensemble.N, 3))*100 #100にセット
    print("=100\n", ensemble.positions)

    print("速度の配列\n", ensemble.velocities)

def main():
    ATOM_NUM = 1
    CYCLE_NUM = 50

    paricles = [Particle() for i in range(ATOM_NUM)]

    ensemble = Ensemble(paricles)
    ensemble.positions += 2

    print("初期位置\n", ensemble.positions)
    print("初速度\n", ensemble.velocities)

    myfield = Field(ensemble, dt=0.01)
    for i in range(CYCLE_NUM):
        myfield.update()

        print("t:", myfield.dt*(i+1))
        print("x:", myfield.ensemble.positions)
        print("v:", myfield.ensemble.velocities)
        print()


if __name__=="__main__":
    main()
