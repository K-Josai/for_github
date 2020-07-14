import numpy as np

class Particle:
    def __init__(self, position=None, velocity=None, mass=None):
        """
        position : np.array (3)
            位置（デフォルト[0, 0, 0]）

        velocity : np.array (3)
            速度（デフォルト[0, 0, 0]）

        mass : float
            質量（デフォルト 1）
        """
        zeros = np.zeros((3), dtype=np.float64)
        
        self.position = position if (position is not None) else zeros
        self.velocity = velocity if (velocity is not None) else zeros
        
        self.mass = mass if ( mass is not None) else 1.0
