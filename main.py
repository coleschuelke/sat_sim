import os
from datetime import datetime

import numpy as np

import config as cfig
from core import DataLogger, PhysicsEngine
from objects import Satellite
from utils import Quaternion

# The main caller script for my satellite simulation

# Main loop
def main():
    # Initialize the sim
    output_path = os.path.join("data", f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    logger = DataLogger(output_path)

    engine = PhysicsEngine()

    sat1 = Satellite( # update these inits with attitude
        name='Sat1', 
        mass=500, 
        inertia=np.diag([500, 500, 600]), 
        position=np.array((0, 0, 1500000 + cfig.EARTH_RADIUS)), 
        velocity=np.array((9000, 0, 0)),
        attitude=Quaternion(1, 0, 0, 0),
        angular_velocity=[0.3, 0.05, 0.1]
    )
    sat2 = Satellite(
        name='Sat2', 
        mass=500, 
        inertia=np.diag([400, 300, 500]), 
        position=np.array((0, 0, 400000 + cfig.EARTH_RADIUS)), 
        velocity=np.array((7800*np.cos(45), 7800*np.sin(45), 0)),
        attitude=Quaternion(1, 2, 3, 4),
        angular_velocity=[0.3, 0.0, 0.1]
    )

    constellation = [sat1, sat2]

    # GNC step

    # Physics step
    try:
        print(f"Running Sim")
        logger.log_step(-1, sat1)
        logger.log_step(-1, sat2)

        t = cfig.T0
        while t < cfig.TF:
            for sat in constellation:
                # Step the phyics
                engine.propagate(sat, t, cfig.DT)

                # Log the telemetry
                logger.log_step(t, sat)


            t += cfig.DT

    finally:
        logger.close()
        print(f"Telemetry saved to {output_path}")


if __name__ == "__main__":
    main()