import numpy as np

class Satellite:
    """
    Docstring for Satellite
    """

    def __init__(self, name, mass, inertia, position, velocity, attitude):
        self.name = name
        self.mass = mass
        self.inertia = np.array(inertia)
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.attitude = np.array(attitude) # Quaternion attitude

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

