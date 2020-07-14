import numpy as np

class Field:
    def __init__(self, ensemble, cel_length=1.0, dt=0.001):
        self.ensemble = ensemble
        self.cel_length = cel_length
        self.dt = dt

    def update(self):
        #自由落下
        g = 9.8
        a = np.array([0, 0, -g])
        x = self.ensemble.positions
        v = self.ensemble.velocities
        t = self.dt
        self.ensemble.positions += v*t + 1/2*a*(t**2)
        self.ensemble.velocities += a*t
        
        self.apply_pbc()

    def apply_pbc(self):
        old_positions = self.ensemble.positions
        new_positions = old_positions
        new_positions[old_positions<0.0] += self.cel_length
        new_positions[old_positions>self.cel_length] -= self.cel_length
        self.ensemble.positions = new_positions
