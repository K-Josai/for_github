import Kshisui as ks
import numpy as np

def main():
    ATOM_NUM = 200 # Number of partics
    DENSITY = 0.8 # NUmber density
    CYCLE_NUM = 50 # Number of Cycle
    DT = 0.000001 # Time discritization
    R_CUT = 10 # Potencital Cutoff
    
    init_positions = np.random.rand(ATOM_NUM, 3) * 5
    init_positions[:,2] = 0
    #init_positions = np.array([[0, 1, 0], [0, 0, 0], [0, 2, 0]])
    paricles = [ks.Particle(position=init_positions[i], mass=1) for i in range(ATOM_NUM)]

    ensemble = ks.Ensemble(paricles)

    myfield = ks.LennardJonesField(ensemble, rho=DENSITY, dt=DT)
    position_recorder = np.zeros((ATOM_NUM, 3, CYCLE_NUM))
    print("Cycle start")
    for i in range(CYCLE_NUM):
        position_recorder[:,:,i] = myfield.ensemble.positions
        myfield.update()
        
        ks.show_progress(i, CYCLE_NUM)

    print("Draw GIF")
    x = position_recorder[:,0,:]
    y = position_recorder[:,1,:]
    ks.drawMolecularAnimation2D(x, y, cel_length=np.sqrt(float(ATOM_NUM/DENSITY)))

if __name__=="__main__":
    main()
