import os
from datetime import datetime

import numpy as np

import config as cfig
from core import DataLogger, PhysicsEngine
from objects import Satellite

# The main caller script for my satellite simulation

# Main loop
def main():
    # Initialize the sim
    output_path = os.path.join("data", f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    logger = DataLogger(output_path)

    engine = PhysicsEngine()

    sat = Satellite(
        'Sat1', 
        500, 
        np.zeros((4, 4)), 
        np.array([0, 0, 2000000 + cfig.EARTH_RADIUS]), 
        np.array([7800, 0, 0]),
        np.zeros(4)
    )

    # GNC step

    # Physics step
    try:
        print(f"Running Sim")

        t = cfig.T0
        while t < cfig.TF:
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