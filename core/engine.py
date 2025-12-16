import numpy as np
from scipy.integrate import solve_ivp
import config
from utils import Quaternion


class PhysicsEngine:
    """
    Docstring for PhysicsEngine
    """
    @staticmethod
    def calculate_gravity(position):
        """
        Calculates the gravitational acceleration including the J2 perturbation
        
        :param position: Description
        """
        x, y, z = position 
        r_sq = x**2 + y**2 + z**2
        r_mag = np.sqrt(r_sq)
        mu_r3 = (config.G * config.EARTH_MASS) / (r_mag**3)

        j2_factor = 1.5 * config.J2 * (config.EARTH_RADIUS / r_mag)**2

        z2_r2 = 5 * (z**2 / r_sq)

        txy = 1 + j2_factor * (1 - z2_r2)
        tz = 1 + j2_factor * (3 - z2_r2)

        ax = -mu_r3 * x * txy
        ay = -mu_r3 * y * txy
        az = -mu_r3 * z * tz

        return np.array([ax, ay, az])
    
    def eom(self, t, x, entity): # Can add control input later
        """
        Equations of Motion. General for now, could become entity specific later
        
        :param self: Description
        :param t: Description
        :param x: Description
        :param mass: Description
        """
        position = x[0:3]
        velocity = x[3:6]
        attitude = Quaternion(*x[6:10]) # Normalized at initialization
        omega = x[10:13]

        # Linear
        acc_gravity = self.calculate_gravity(position)

        thrust_force = entity.get_thrust_vector(current_velocity=velocity)
        acc_thrust = thrust_force / entity.mass

        total_acc = acc_gravity + acc_thrust

        # Rotational
        q_dot = attitude.rate_of_change(omega)
        torque = np.zeros(3) # No current sources of angular velocity

        I = entity.inertia
        H = I @ omega

        alpha = np.linalg.inv(I) @ (torque - np.cross(omega, H))

        dxdt = np.concatenate((velocity, total_acc, q_dot, alpha))

        return dxdt
    
    def propagate(self, entity, t, dt):
        """
        Updates the state of an entity according to the physics applied over dt
        
        :param self: Description
        :param entity: Description
        :param dt: Description
        """
        x0 = np.concatenate((entity.position, entity.velocity, entity.attitude.q, entity.angular_velocity))
        
        sol = solve_ivp(
            fun=self.eom,
            t_span=(t, t+dt),
            y0=x0,
            method='RK45', 
            args=(entity,), 
            rtol=1e-6,
            atol=1e-9    
        )

        final_state = sol.y[:, -1]
        final_positon = final_state[0:3]
        final_velocity = final_state[3:6]
        final_attitude = final_state[6:10]
        final_angular_velocity = final_state[10:13]

        entity.position = final_positon
        entity.velocity = final_velocity
        entity.attitude = Quaternion(*final_attitude)
        entity.angular_velocity = final_angular_velocity