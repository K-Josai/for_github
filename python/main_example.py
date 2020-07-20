import numpy as np
import pandas as pd
import sys

# --------------------------------------------------------
PI = 3.1415926535897
# Dimention=2
# NOF0=11, NOF1=12, NOF2=13, NOF3=14

NATOM = 10  # Number of particles
NRHO = 0.8  # Number density
LCEL = np.sqrt(float(NATOM/NRHO))  # Box Size
L2 = LCEL/2.0

RCUT = 4.0  # Potential Cutoff
NCYCLE = 10  # Number of Cycle
NPRINT = 1  # How often print the configurations
DT = 0.001  # Time discritization
TTEMP = 0.0  # Target temperature

# --------------------------------------------------------
# periodic boundary condition
# r: matrix [x-coordinates, y-coordinates]


def pbc(r):
    x = r[0]
    y = r[1]
    for i in range(NATOM):
        if x[i] < 0.0:
            x[i] = x[i] + LCEL
        elif x[i] > LCEL:
            x[i] = x[i] - LCEL

        if y[i] < 0.0:
            y[i] = y[i] + LCEL
        elif y[i] > LCEL:
            y[i] = y[i] - LCEL
    r_new = np.array([x, y])
    return r_new


# calculation of velocity
# u: matrix [x-velocities, y-velocities]
def calcu(u0, F, T1):
    u = u0 + T1*F
    return u


# caluculation of position
def calcr(r0, u, T1):
    r = r0+T1*u
    return r


# calculation of forces
def calcF(r):
    x = r[0]
    y = r[1]
    pot = 0.0
    virial = 0.0
    Fx = np.zeros(NATOM)
    Fy = np.zeros(NATOM)
    # two particles i and j (i<j)
    for i in range(NATOM):
        for j in range(i+1, NATOM):
            xij = x[j] - x[i]
            if xij > L2:
                xij = xij - LCEL
            elif xij < -L2:
                xij = xij + LCEL

            yij = y[j] - y[i]
            if yij > L2:
                yij = yij-LCEL
            elif yij < -L2:
                yij = yij+LCEL

            # distance of two particles i and j
            rij = np.sqrt(xij**2+yij**2)

            # Lennard-Jones Potential
            Eij = 0
            Fij = 0
            if rij <= RCUT:
                Eij = 4.0*(rij**(-12)-rij**(-6))
                Fij = 24.0*(-2.0*rij**(-13)+rij**(-7))
                pot = pot+Eij
                virial = virial+Fij*rij

                Fx[i] += Fij*xij/rij
                Fy[i] += Fij*yij/rij
                Fx[j] -= Fij*xij/rij
                Fy[j] -= Fij*yij/rij
    F = np.array([Fx, Fy])
    result = np.array([F, pot, virial])
    return result


# makes initial structures
def INITIAL(seed_):
    np.random.seed(seed=seed_)
    print("Make Structures")
    NCEL = 1+int(np.sqrt(float(NATOM)))

    # initial position of the particles
    x = np.zeros(NATOM)
    y = np.zeros(NATOM)
    ux = np.zeros(NATOM)
    uy = np.zeros(NATOM)
    i = 0
    for ix in range(NCEL):
        if i >= NATOM:
            break
        for iy in range(NCEL):
            if i >= NATOM:
                break
            x[i] = (float(ix)+0.5)*LCEL/(float(NCEL))
            y[i] = (float(iy)+0.5)*LCEL/(float(NCEL))
            i += 1

    # initial velocity of the particles
    SDB = 1.0
    r1 = np.random.rand(NATOM)
    r2 = np.random.rand(NATOM)
    ux = SDB*np.sqrt(-2.0*np.log(r1))*np.cos(2.0*PI*r2)  # あとで検討する
    uy = SDB*np.sqrt(-2.0*np.log(r1))*np.sin(2.0*PI*r2)

    # Initialize total momentum
    uxsum = np.sum(ux)
    uysum = np.sum(uy)
    print("total momentum before initialization", uxsum, uysum)
    ux = ux-uxsum/float(NATOM)
    uy = uy-uysum/float(NATOM)
    uxsum = np.sum(ux)
    uysum = np.sum(uy)
    print("new total momentum", uxsum, uysum)
    r = np.array([x, y])
    u = np.array([ux, uy])
    return np.array([r, u])


def INITIAL_READ():
    df = pd.read_csv(
        "start.txt", delim_whitespace=True, header=None, skiprows=1)
    print("pandas data frame")

    data_ndarray = df.values
    print(data_ndarray.shape)

    r = np.array([data_ndarray[:, 0], data_ndarray[:, 1]])
    u = np.array([data_ndarray[:, 2], data_ndarray[:, 3]])
    return np.array([r, u])


# velocity-Verlet
def VVcycle(r_old, u_old):
    forces_old = calcF(r_old)
    u_img = calcu(u_old, forces_old[0], DT/2.0)
    r_new = pbc(calcr(r_old, u_img, DT))
    forces_new = calcF(r_new)
    u_new = calcu(u_img, forces_new[0], DT/2.0)

    temp = (np.sum((u_new[0]**2)+(u_new[1]**2))/2.0)/float(NATOM)
    # mean kinetic energy
    pot = forces_new[1]/float(NATOM)  # mean potential energy
    virial = (float(NATOM)*temp-forces_new[2]/2.0)/(LCEL**2)  # virial #あとで検討する
    energy = temp+pot  # mean mechanical energy
    observables = np.array([temp, pot, virial, energy])  # physical quantities
    result = np.array([r_new, u_new, forces_new, observables])
    return result


# --------------------------------------------------------
def main():
    state = INITIAL(1)
    print(calcF(state[0]))
    average = np.zeros(4)
    with open("./log_py.txt", "w") as f:
        print("NATOM={}".format(NATOM), file=f)
        for NSTEP in range(NCYCLE):
            sys.stdout.write("\r{}".format(NSTEP))
            sys.stdout.flush()
            VVresult = VVcycle(state[0], state[1])
            state = [VVresult[0], VVresult[1]]

            if NSTEP % NPRINT == 0:
                print("{} {}".format(NSTEP*DT, VVresult[3]), file=f)

            # time average of physical quantities after sufficient time
            if NSTEP >= NCYCLE/2:
                average += VVresult[3]/(float(NCYCLE)/2)

    # FIN
    print("\n TEMP POT ENERGY VIRIAL")
    print(average)
    # for i in range(NATOM): 座標を出力


if __name__ == "__main__":
    main()
