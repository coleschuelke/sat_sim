import numpy as np
import config
from utils import Quaternion

class Environment:
    def get_forces(self, t, state, body):
        """
        Docstring for get_derivative
        
        :param self: Description
        :param t: Description
        :param state: Description
        """
        raise NotImplementedError
    def get_torques(self, t, state, body):
        """
        Docstring for get_torques
        
        :param self: Description
        :param t: Description
        :param state: Description
        :param body: Description
        """
        raise NotImplementedError

class TwoBodyJ2(Environment):
    """
    Docstring for LEO
    """
    def __init__(self, radius, mass, j2):
        self.mass = mass
        self.radius = radius
        self.j2 = j2

    def get_forces(self, t, state, body):
        """
        Docstring for get_derivative
        
        :param self: Description
        :param t: Description
        :param state: Description
        """
        r_vec = state[0:3]
        velocity = state[3:6]
        attitude = Quaternion(*state[6:10]) # Normalized at initialization
        omega = state[10:13]

        # Precomputations
        x, y, z = r_vec
        r_sq = x**2 + y**2 + z**2
        r_mag = np.sqrt(r_sq)
        m_body = body.mass
        mu_r3 = config.G * self.mass * m_body / (r_mag**3)
        j2_factor = 1.5 * self.j2 * config.G * self.mass * (self.radius**2) * m_body # Multiply by mass to get force
        zr2 = (z**2) / r_sq
        r5 = r_mag**5

        # Central gravity
        f_gravity = -mu_r3 * r_vec

        # J2
        t_xy = -j2_factor * (1 - 5*zr2) / r5
        t_z = -j2_factor * (3 - 5*zr2) / r5

        f_j2 = np.array([t_xy * x, t_xy * y, t_z * z])

        # TODO: Drag
        # TODO: SRP

        # Sum all forces
        total_force = f_gravity + f_j2 # In the inertial frame

        return total_force
    
    def get_torques(self, t, state, body):
        """
        Docstring for get_torques
        
        :param self: Description
        :param t: Description
        :param state: Description
        :param body: Description
        """
        r_inertial = state[0:3]
        attitude = Quaternion(*state[6:10])
        I = body.inertia
        mu = config.G * config.EARTH_MASS
        r5 = np.linalg.norm(r_inertial) ** 5
        r_body = attitude.conjugate().rotate_vector(r_inertial)

        tau_gg = 3*mu * np.cross(r_body, I @ r_body) / r5

        tau_total = tau_gg
        
        # TODO: Drag

        return tau_total


class CR3BP(Environment):
    """
    Docstring for EarthMoonCR3BP
    """
    def __init__(self, mu_param):
        self.mu_param = mu_param # Mass ratio
    def get_forces(self, t, state, body):
        """
        Docstring for get_derivative
        
        :param self: Description
        :param t: Description
        :param state: Description
        """
        raise NotImplementedError
    
    def get_torques(self, t, state, body):
        """
        Docstring for get_torques
        
        :param self: Description
        :param t: Description
        :param state: Description
        :param body: Description
        """
        raise NotImplementedError