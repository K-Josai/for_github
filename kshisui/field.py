import numpy as np
import warnings

class Field:
    def __init__(self, ensemble, rho=0.8, r_cut=8, dt=0.001):
        """
        ensemble : Ensemble object
            粒子集団

        rho : float
            Number density

        r_cut : float
            Potential Cutoff

        dt : float
            Time discritization 時間刻み幅
        """
        self.ensemble = ensemble
        self.N = self.ensemble.N
        
        self.rho = rho
        self.r_cut = r_cut
        self.dt = dt
        
        self.cel_length = np.sqrt(float(self.N/self.rho))
        self.cel_half_length = self.cel_length*0.5

        self.apply_pbc() # 最初にPBCsを適用しておく

    def update(self):
        pass

    def apply_pbc(self):
        """
        Apply Periodic boundary conditions (PBCs)
        
        NOTE: 1セルの大きさより大きく移動した場合は，正しく適用されないので注意
        """
        positions = self.ensemble.positions
        lower_positions = (positions<0.0)
        upper_positions = (positions>=self.cel_length)
        positions[lower_positions] += self.cel_length
        positions[upper_positions] -= self.cel_length
        self.ensemble.positions = positions
        
        # チェック用
        lower_positions = (positions<0.0)
        upper_positions = (positions>=self.cel_length)
        if np.any(lower_positions) or np.any(upper_positions):
            warning_msg = "\nOops!: Some of the particles have shifted significantly.\n       Be careful. PBCs may not be maintained."
            warnings.warn(warning_msg)


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

class LennardJonesField(Field):
    def update(self):
        self.VelocityVerlet()
        self.apply_pbc()

    def LennardJones_Force(self, r, sigma, epsilon):
        return 4*epsilon * ( 12*(sigma**12)/(r**13) - 6*(sigma**6)/(r**7) )

    def calc_force(self):
        """
        粒子にかかる力の計算

        １．粒子間距離(rij)とベクトル(ri-rj)を取得
        ２．カットオフで必要な粒子のみ抽出
        ３．抽出した粒子から，粒子の組み合わせごとのLennard-Jonesを計算
        ４．抽出した粒子を統合して，各粒子にかかる力を求める
        """
        r = self.ensemble.get_distance_map() # 粒子間距離(rij)
        vec = self.ensemble.get_posi_vec_map() #粒子間位置のベクトル(ri-rj)
        
        index2preserve = np.logical_and(0<r, r<=self.r_cut) # カットオフして計算に用いる粒子の組み合わせ(True->残す，False->カットオフ)
        # 0<r は同一粒子の組み合わせなのでカット

        r_preserved = r[index2preserve] # カットオフ後の粒子間距離
        vec_preserved = vec[index2preserve] # カットオフ後の粒子間ベクトル

        # 各粒子同士のLennard-Jonesポテンシャルでの力を計算
        epsilon = 1
        sigma = 1
        F_preserved = (self.LennardJones_Force(r_preserved, sigma, epsilon) * -vec_preserved.T / r_preserved).T

        # 各粒子同士にかかる力のマップ
        # カットオフした粒子の組み合わせは0になっている
        F_map = np.zeros_like(vec)
        F_map[index2preserve] = F_preserved
        
        # F_mapを列ごとに足し合わせる
        # これが，全ての粒子の影響を考慮した力になる
        F = np.sum(F_map, axis=0)
        return F
    
    def VelocityVerlet(self):
        F = self.calc_force()

        q = self.ensemble.positions
        v = self.ensemble.velocities
        dt = self.dt
        M = self.ensemble.mass[..., None]

        self.ensemble.positions = q + v*dt + F/M*(dt**2)/2

        self.apply_pbc()
        F_dt = self.calc_force()
        self.ensemble.velocities = v + dt/2 * (F + F_dt) / M
