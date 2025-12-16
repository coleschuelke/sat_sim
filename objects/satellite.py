import numpy as np
from utils import Quaternion

class Satellite:
    """
    Docstring for Satellite
    """

    def __init__(self, name, mass, inertia, position, velocity, attitude=None, angular_velocity=None):
        self.name = name
        self.mass = mass
        self.inertia = np.array(inertia)
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        if attitude is None:
            self.attitude = Quaternion()
        elif isinstance(attitude, (list, np.ndarray, tuple)):
            self.attitude = Quaternion(*attitude)
        else:
            self.attitude = attitude

        # Angular Velocity in the body frame
        if angular_velocity is None:
            self.angular_velocity = np.zeros(3)
        else:
            self.angular_velocity = np.array(angular_velocity)

        # Define the state
        self.state = np.concatenate((self.position, self.velocity))


    def get_thrust_vector(self, current_velocity=None): # TODO: This should really be attitude, not velocity eventually
        """
        Gets the thrust vector using the current velocity vector for propagation
        
        :param self: Description
        :param current_velocity: Description
        """
        # TODO: Write this function
        return np.zeros(3)

