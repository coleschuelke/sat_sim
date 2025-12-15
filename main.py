import numpy as np

# The main caller script for my satellite simulation


# Sim params
t0 = 0 # s
tf = 1000 # s

est_freq = 10 # Hz
cont_freq = 5 # Hz

dt = 0.1 # will later be a function of other paramters

# Main loop
for t in range(t0, tf, dt):
    pass

    # Propagate the sim

    # Take sensor measurements

    # Run the estimator

    # Run the controller