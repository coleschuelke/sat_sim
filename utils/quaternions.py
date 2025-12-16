import numpy as np

class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        # We store it as a numpy array for easy math later
        # Order: [w, x, y, z] (Scalar first is standard in physics/engineering)
        self.q = np.array([w, x, y, z], dtype=float)
        self.normalize()

    def normalize(self):
        """Ensures the quaternion has unit magnitude."""
        norm = np.linalg.norm(self.q)
        if norm > 1e-9:
            self.q /= norm
        else:
            # Fallback to identity if we get a zero vector (avoids NaN)
            self.q = np.array([1.0, 0.0, 0.0, 0.0])

    def rotate_vector(self, vector):
        """
        Rotates a 3D vector using this quaternion.
        Formula: v' = q * v * q_conjugate
        """
        # 1. Convert vector to pure quaternion (0, vx, vy, vz)
        v_quat = Quaternion(0, vector[0], vector[1], vector[2])
        
        # 2. q * v
        temp = self @ v_quat
        
        # 3. (q * v) * q_inv
        rotated = temp @ self.conjugate()
        
        # Return just the vector part (x, y, z)
        return rotated.q[1:]

    def conjugate(self):
        """Returns the inverse rotation."""
        w, x, y, z = self.q
        return Quaternion(w, -x, -y, -z)

    def __matmul__(self, other):
        """
        Implements the '@' operator for Quaternion Multiplication (Hamilton Product).
        """
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = other.q
        
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        
        # Return a new Quaternion object (auto-normalized by init)
        return Quaternion(w, x, y, z)

    def __repr__(self):
        return f"Quat({self.q[0]:.3f}, [{self.q[1]:.3f}, {self.q[2]:.3f}, {self.q[3]:.3f}])"

    @staticmethod
    def from_axis_angle(axis, angle_rad):
        """Factory method to create a quaternion from a rotation axis and angle."""
        axis = np.array(axis)
        norm = np.linalg.norm(axis)
        if norm < 1e-9:
            return Quaternion() # Identity
            
        axis = axis / norm
        half_angle = angle_rad / 2.0
        
        w = np.cos(half_angle)
        xyz = axis * np.sin(half_angle)
        
        return Quaternion(w, xyz[0], xyz[1], xyz[2])
    
    def rate_of_change(self, omega_vector):
        """
        Calculates q_dot = 0.5 * q * omega
        
        :param omega_vector: Angular velocity (rad/s) in BODY frame [wx, wy, wz]
        :return: A numpy array representing dq/dt (4 elements)
        """
        # Convert angular velocity vector to a pure quaternion (0, wx, wy, wz)
        w_quat = Quaternion(0, *omega_vector)
        
        # Apply the kinematic equation: q_dot = 0.5 * q * w
        # Note: We use self @ w_quat because the omega is usually in the Body frame
        # If omega is in Inertial frame, use w_quat @ self
        q_dot = (self @ w_quat).q * 0.5
        
        return q_dot
    
    def to_euler(self):
        """
        Returns (roll, pitch, yaw) in radians for this instance.
        Sequence: Z-Y-X (3-2-1) Aero standard.
        """
        return Quaternion.quat_to_euler(self.q)

    @staticmethod
    def quat_to_euler(q_array):
        """
        Vectorized conversion of Quaternions to Euler Angles (Roll, Pitch, Yaw).
        Works for single quaternion (4,) or array of quaternions (N, 4).
        
        :param q_array: numpy array of shape (4,) or (N, 4) [w, x, y, z]
        :return: (roll, pitch, yaw) in radians
        """
        # Ensure input is at least 1D array
        q = np.atleast_2d(q_array)
        
        w, x, y, z = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
        
        # Roll (x-axis rotation)
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = np.arctan2(t0, t1)
        
        # Pitch (y-axis rotation)
        t2 = +2.0 * (w * y - z * x)
        # Clamp to [-1, 1] to avoid NaNs from floating point noise
        t2 = np.clip(t2, -1.0, 1.0) 
        pitch = np.arcsin(t2)
        
        # Yaw (z-axis rotation)
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = np.arctan2(t3, t4)
        
        # If input was 1D, return 1D result
        if q_array.ndim == 1:
            return np.array([roll[0], pitch[0], yaw[0]])
            
        return np.column_stack((roll, pitch, yaw))