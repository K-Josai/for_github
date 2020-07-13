from particle import Particle
from ensemble import Ensemble
import numpy as np

def main():
    NATOM = 2

    paricles = [Particle() for i in range(NATOM)]

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

if __name__=="__main__":
    main()
