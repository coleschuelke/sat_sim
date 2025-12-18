import os
from datetime import datetime

import numpy as np

import config as cfig
from core import DataLogger, PhysicsEngine
from objects import Satellite
from utils import Quaternion
from environments import TwoBodyJ2

# The main caller script for my satellite simulation

# Main loop
def main():
    # Initialize the sim
    output_path = os.path.join("data", f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    logger = DataLogger(output_path)

    env = TwoBodyJ2(cfig.EARTH_RADIUS, cfig.EARTH_MASS, cfig.EARTH_J2)

    engine = PhysicsEngine(env)

    sat1 = Satellite(
        name='Sat1', 
        mass=500, 
        inertia=np.diag([10, 10, 2]), 
        position=np.array((0, 0, 1500000 + cfig.EARTH_RADIUS)), 
        velocity=np.array((9000, 0, 0)),
        attitude=Quaternion(1, 2, 3, 4),
        angular_velocity=[0.000, 0.000, 0.000]
    )
    sat2 = Satellite(
        name='Sat2', 
        mass=500, 
        inertia=np.diag([400, 300, 500]), 
        position=np.array((0, 0, 400000 + cfig.EARTH_RADIUS)), 
        velocity=np.array((7800*np.cos(45), 7800*np.sin(45), 0)),
        attitude=Quaternion(1, 2, 3, 4),
        angular_velocity=[1e-6, 3e-6, -1e-6]
    )

    constellation = [sat1, sat2]

    try:
        print(f"Running Sim")
        logger.log_step(-1, sat1)
        logger.log_step(-1, sat2)

        t = cfig.T0
        while t < cfig.TF:
            for sat in constellation:
                # GNC Step

                # Physics Step
                engine.propagate(sat, t, cfig.DT)

                # Log the telemetry
                logger.log_step(t, sat)


            t += cfig.DT

    finally:
        logger.close()
        print(f"Telemetry saved to {output_path}")


if __name__ == "__main__":
    main()