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
        for i, particle in enumerate(self.paricles):
            positions[i] = particle.position
        return positions

    @positions.setter
    def positions(self, positions_dst):
        for i in range(self.N):
            self.paricles[i].position = positions_dst[i]
    
    @property
    def velocities(self):
        velocities = np.zeros((self.N, 3), dtype=np.float32)
        for i, particle in enumerate(self.paricles):
            velocities[i] = particle.velocity
        return velocities
    
    @velocities.setter
    def velocities(self, velocities_dst):
        for i in range(self.N):
            self.paricles[i].velocity = velocities_dst[i]
