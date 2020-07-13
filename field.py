import numpy as np

class Field:
    def __init__(self, ensemble, dt=0.001):
        self.ensemble = ensemble
        self.dt = dt

    def update(self):
        #自由落下
        g = 9.8
        a = np.array([0, 0, -g])
        x = self.ensemble.positions
        v = self.ensemble.velocities
        t = self.dt
        self.ensemble.positions += v*t + 1/2*a*(t**2)
        self.ensemble.velocities += v + a*t
