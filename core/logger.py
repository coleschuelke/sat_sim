import csv
import os

class DataLogger:
    def __init__(self, filepath, mode='w'):
        self.filepath = filepath
        
        # Safety: Create directory if it doesn't exist (e.g., 'results/')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Keep file open for performance (vs opening/closing every step)
        self.file = open(filepath, mode, newline='')
        self.writer = csv.writer(self.file)
        
        # Write Header immediately
        self.writer.writerow([
            'time', 'name',
            'rx', 'ry', 'rz', 
            'vx', 'vy', 'vz',
            'qw', 'qx', 'qy', 'qz',    # <--- NEW: Quaternion
            'wx', 'wy', 'wz',          # <--- NEW: Angular Velocity
            'mass', 'thrust_on'
        ])

    def log_step(self, time, satellite):
        rx, ry, rz = satellite.position
        vx, vy, vz = satellite.velocity
        qw, qx, qy, qz = satellite.attitude.q
        wx, wy, wz = satellite.angular_velocity
        
        row = [
            time, satellite.name,
            rx, ry, rz,
            vx, vy, vz,
            qw, qx, qy, qz,   # <--- Log them
            wx, wy, wz,       # <--- Log them
            satellite.mass,
            0
            # int(satellite.thrust_is_on)
        ]
        self.writer.writerow(row)

    def close(self):
        """Flush and close the file handler."""
        self.file.close()