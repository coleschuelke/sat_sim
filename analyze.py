import argparse

import matplotlib.pyplot as plt

# Import the functions directly
from visualization.plotter import load_data, plot_orbit_3d, plot_telemetry

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    
    # 1. Load
    df = load_data(args.file)
    
    # 2. Plot
    print("Showing Telemetry...")
    plot_telemetry(df)
    
    print("Showing 3D Orbit...")
    # We can handle the figure creation here if we want more control
    plot_orbit_3d(df)
    plt.show()