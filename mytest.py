from particle import Particle
from ensemble import Ensemble
from field import Field, FreeFallField
import numpy as np

def main():
    ATOM_NUM = 1 # Number of particles
    CYCLE_NUM = 50 # Number of Cycle

    paricles = [Particle() for i in range(ATOM_NUM)]

    ensemble = Ensemble(paricles)
    ensemble.positions += 2

    print("初期位置\n", ensemble.positions)
    print("初速度\n", ensemble.velocities)

    myfield = FreeFallField(ensemble, dt=0.05)
    for i in range(CYCLE_NUM):
        myfield.update()

        print("t:", myfield.dt*(i+1))
        print("x:", myfield.ensemble.positions)
        print("v:", myfield.ensemble.velocities)
        print()


if __name__=="__main__":
    main()
