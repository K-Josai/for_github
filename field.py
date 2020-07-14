import numpy as np

class Field:
    def __init__(self, ensemble, rho=0.8, dt=0.001):
        self.ensemble = ensemble
        self.N = self.ensemble.N
        
        self.rho = rho
        self.dt = dt
        
        self.cel_length = np.sqrt(float(self.N/self.rho))
        self.cel_half_length = self.cel_length*0.5

    def update(self):
        pass

    def apply_pbc(self):
        """
        Apply Periodic boundary conditions (PBCs)
        
        NOTE: 1セルの大きさより大きく移動した場合は，正しく適用されない
        """
        old_positions = self.ensemble.positions
        new_positions = old_positions
        new_positions[old_positions<0.0] += self.cel_length
        new_positions[old_positions>self.cel_length] -= self.cel_length
        self.ensemble.positions = new_positions


class FreeFallField(Field):
    """
    自由落下の環境
    z軸負の方向に重力加速度g
    """
    def update(self):
        g = 9.8
        a = np.array([0, 0, -g])
        v = self.ensemble.velocities
        t = self.dt
        self.ensemble.positions += v*t + 1/2*a*(t**2)
        self.ensemble.velocities += a*t
        
        self.apply_pbc()

class MDField(Field):
    def update(self):
        pass

    def VelocityVerlet(self):
        r = self.ensemble.positions
        v = self.ensemble.velocities
