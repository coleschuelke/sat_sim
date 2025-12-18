import numpy as np
from scipy.integrate import solve_ivp
import config
from utils import Quaternion


class PhysicsEngine:
    """
    Docstring for PhysicsEngine
    """
    def __init__(self, env):
        self.env = env
    
    def eom(self, t, x, body): # Can add control input later
        """
        Equations of Motion IN THE INERTIAL FRAME
        
        :param self: Description
        :param t: Description
        :param x: Description
        :param mass: Description
        """
        position = x[0:3]
        velocity = x[3:6]
        attitude = Quaternion(*x[6:10]) # Normalized at initialization
        omega = x[10:13]

        # Constants
        I = body.inertia
        H = I @ omega

        # Sum forces
        env_forces = self.env.get_forces(t, x, body)
        control_forces = np.zeros(3)

        total_forces = env_forces + control_forces
        
        # Sum torques
        env_torques = self.env.get_torques(t, x, body)
        control_torques = np.zeros(3)

        total_torques = env_torques + control_torques

        # Dynamics
        v_dot = total_forces / body.mass
        omega_dot = np.linalg.inv(I) @ (total_torques - np.cross(omega, H))

        # Kinematics
        r_dot = velocity
        q_dot = attitude.rate_of_change(omega)

        # Derivative of state for integration
        dxdt = np.concatenate((r_dot, v_dot, q_dot, omega_dot))

        return dxdt
    
    def propagate(self, body, t, dt):
        """
        Updates the state of an body according to the physics applied over dt
        
        :param self: Description
        :param body: Description
        :param dt: Description
        """
        x0 = np.concatenate((body.position, body.velocity, body.attitude.q, body.angular_velocity))
        
        sol = solve_ivp(
            fun=self.eom,
            t_span=(t, t+dt),
            y0=x0,
            method='RK45', 
            args=(body,), 
            rtol=1e-6,
            atol=1e-9    
        )

        final_state = sol.y[:, -1]
        final_positon = final_state[0:3]
        final_velocity = final_state[3:6]
        final_attitude = final_state[6:10]
        final_angular_velocity = final_state[10:13]

        body.position = final_positon
        body.velocity = final_velocity
        body.attitude = Quaternion(*final_attitude)
        body.angular_velocity = final_angular_velocity