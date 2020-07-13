from particle import Particle
from ensemble import Ensemble

def main():
    NATOM = 10

    paricles = [Particle() for i in range(NATOM)]

    ensemble = Ensemble(paricles)

    print("位置の配列\n", ensemble.positions)
    
    print("速度の配列\n", ensemble.velocities)

if __name__=="__main__":
    main()
