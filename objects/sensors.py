import numpy as np
from utils.quaternions import Quaternion


class Sensor:
    def __init__(
        self,
        name,
        satellite,
        meas_rate,
        noise_var=1.0,
        bias=0.0,
        mount_q=Quaternion(1, 0, 0, 0),
    ):
        self.name = name
        self.satellite = satellite
        self.meas_rate = meas_rate
        self.last_update_time = -1
        self.dt = 1 / meas_rate
        self.var = noise_var
        self.bias = bias
        self.mount_q = mount_q

    def measure(self, t):
        if t - self.last_update_time < self.dt:
            return None  # Not time to get a new measurement

        tv = self.get_true_value()
        trans_tv = self.apply_mounting(tv)
        meas = self.apply_noise(trans_tv)
        return meas

    def get_true_value(self):
        return NotImplementedError

    def apply_mounting(self, val):
        if isinstance(val, np.ndarray) and len(val) == 3:
            return self.mount_q.conjugate().rotate_vector(val)
        elif isinstance(val, Quaternion):
            return self.mount_q.conjugate() * val
        else:
            return val

    def apply_noise(self, val):
        if isinstance(val, np.ndarray):
            noise = np.random.normal(self.bias, np.sqrt(self.var), val.shape)
            return val + noise
        elif isinstance(val, Quaternion):
            angle_error = np.random.normal(0, self.var, size=3)
            q_err = Quaternion.from_euler(*angle_error)
            return q_err * val


class Gyro(Sensor):
    def get_true_value(self):
        return self.satellite.omega


class StarTracker(Sensor):
    def get_true_value(self):
        return self.satellite.attitude


class GPS(Sensor):
    def get_true_value(self):
        return self.satellite.position
