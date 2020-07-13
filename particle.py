import numpy as np

class Particle:
    def __init__(self, position=None, velocity=None):
        zeros = np.zeros((3), dtype=np.float32)
        
        self.position = position if (position is not None) else zeros
        self.velocity = velocity if (velocity is not None) else zeros
