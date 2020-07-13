import numpy as np

class Ensemble:
    def __init__(self, particles):
        self.paricles = particles

    @property
    def N(self):
        return len(self.paricles)

    @property
    def positions(self):
        positions = np.zeros((self.N, 3), dtype=np.float32)
        for i, paricle in enumerate(self.paricles):
            positions[i] = paricle.position
        return positions
    
    @property
    def velocities(self):
        velocities = np.zeros((self.N, 3), dtype=np.float32)
        for i, paricle in enumerate(self.paricles):
            velocities[i] = paricle.velocity
        return velocities
