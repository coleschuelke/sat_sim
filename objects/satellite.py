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

