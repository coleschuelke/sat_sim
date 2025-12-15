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
            'time', 
            'rx', 'ry', 'rz',     # Position
            'vx', 'vy', 'vz',     # Velocity
            'mass', 'thrust_on'   # State
        ])

    def log_step(self, time, entity):
        """
        Extracts state from satellite and writes a row.
        """
        # Unpack numpy arrays for clean CSV writing
        # TODO: use the state in the future
        rx, ry, rz = entity.position
        vx, vy, vz = entity.velocity
        
        row = [
            time,
            rx, ry, rz,
            vx, vy, vz,
            entity.mass,
            # int(satellite.thrust_is_on)
        ]
        self.writer.writerow(row)

    def close(self):
        """Flush and close the file handler."""
        self.file.close()