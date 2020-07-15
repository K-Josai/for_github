import numpy as np

class Ensemble:
    def __init__(self, particles):
        self.paricles = particles

    @property
    def kinetic_energy(self):
        v = self.velocities
        k = 0.5 * np.average(v*v)
        return k

    @property
    def N(self):
        return len(self.paricles)

    @property
    def positions(self):
        positions = np.zeros((self.N, 3), dtype=np.float64)
        for i, particle in enumerate(self.paricles):
            positions[i] = particle.position
        return positions

    @positions.setter
    def positions(self, positions_dst):
        for i in range(self.N):
            self.paricles[i].position = positions_dst[i]
    
    @property
    def velocities(self):
        velocities = np.zeros((self.N, 3), dtype=np.float64)
        for i, particle in enumerate(self.paricles):
            velocities[i] = particle.velocity
        return velocities
    
    @velocities.setter
    def velocities(self, velocities_dst):
        for i in range(self.N):
            self.paricles[i].velocity = velocities_dst[i]
    
    @property
    def mass(self):
        mass = np.zeros((self.N), dtype=np.float64)
        for i, particle in enumerate(self.paricles):
            mass[i] = particle.mass
        return mass
    
    def get_posi_vec_map(self):
        """
        粒子間位置のベクトルのマップ(N,N,3)を計算して返す
        ri - rj
        position difference
        """
        p = self.positions # (N,3)
        N, dim = p.shape[:2]
        
        uti = np.triu_indices(N, k=1)

        dr = p[uti[0]] - p[uti[1]]

        vec_map = np.zeros((N, N, dim))
        vec_map[uti] = dr # 上三角行列のみに値が格納されたマップ
        vec_map_T = -vec_map.transpose((1, 0, 2)) # 下三角行列飲みに値が格納されたマップ（ここで符号は逆転）
        return vec_map + vec_map_T

    def get_distance_map(self):
        """
        粒子間の距離rijマップ(N,N)を計算して返す
        rij = sqrt((rix-rjx)**2 + (riy-rjy)**2 + (riz-rjz)**2))
        
        参考:
        Distance Calculation, http://www.arvindravichandran.com/articles/distance/
        中のCode 2
        """
        p = self.positions # (N,3)
        N = p.shape[0]
        
        # uti is a list of two (1-D) numpy arrays  
        # containing the indices of the upper triangular matrix
        # k=1 eliminates diagonal indices
        uti = np.triu_indices(N, k=1)

        # uti[0] is i, and uti[1] is j from the previous example
        # computes differences between particle positions
        dr = p[uti[0]] - p[uti[1]]

        # computes distances; r is a (N*N-N)/2 x 1 np array
        r = np.sqrt(np.sum(dr*dr, axis=1))
        
        # 計算した距離rは1次元の配列なので，2次元の配列にする
        dist_map = np.zeros((N, N))
        dist_map[uti] = r # 上三角行列のみに値が格納されたマップ
        dist_map_T = dist_map.T # 下三角行列のみに値が格納されたマップ
        return dist_map + dist_map_T
