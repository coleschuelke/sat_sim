import numpy as np
from scipy.integrate import solve_ivp
import config


class PhysicsEngine:
    """
    Docstring for PhysicsEngine
    """
    @staticmethod
    def calculate_gravity(mass, position):
        r_mag = np.linalg.norm(position)
        if r_mag == 0:
            return np.zeros(3)
        
        force_mag = (config.G * config.EARTH_MASS * mass) / (r_mag ** 2)
        force_dir = -position / r_mag
        return force_mag * force_dir
    
    def eom(self, t, x, entity): # Can add control input later
        """
        Equations of Motion. General for now, could become entity specific later
        
        :param self: Description
        :param t: Description
        :param x: Description
        :param mass: Description
        """
        pass
    
    def propagate(self, entity, t, dt):
        """
        Updates the state of an entity according to the physics applied over dt
        
        :param self: Description
        :param entity: Description
        :param dt: Description
        """
        x0 = np.zeros(6)
        
        sol = solve_ivp(
            fun=self.eom,
            t_span=(t, t+dt),
            y0=x0,
            method='RK45', 
            args=(entity.mass), 
            rtol=1e-6,
            atol=1e-9    
        )

        final_state = sol.y[:, -1]
        final_positon = final_state[0:3]
        final_velocity = final_state[3:6]