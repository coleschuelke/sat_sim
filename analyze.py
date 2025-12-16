import argparse
import glob
import os
import sys

import matplotlib.pyplot as plt

# Import your functional plotting library
from visualization.plotter import (animate_orbit, load_data, plot_orbit_3d,
                                   plot_telemetry)


def get_latest_csv(directory="Data"):
    """Finds the most recently modified CSV file in the directory."""
    # Get list of all csv files in 'Data/'
    files = glob.glob(os.path.join(directory, "*.csv"))
    
    if not files:
        return None
    
    # Sort by modification time (newest last)
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Satellite Simulation Results")
    # nargs='?' makes this argument optional
    parser.add_argument('file', nargs='?', type=str, help='Path to CSV file (optional)')
    parser.add_argument('--animate', '-a', action='store_true', help='Enable 3D animation')
    args = parser.parse_args()

    filepath = args.file

    # If no file was provided, find the newest one automatically
    if not filepath:
        print("No file specified. Searching for latest simulation...")
        filepath = get_latest_csv()
        
        if not filepath:
            print("Error: No CSV files found in Data/ directory.")
            sys.exit(1)
            
        print(f"-> Found: {filepath}")

    # --- Loading & Plotting ---
    print(f"Loading data from {filepath}...")
    try:
        df = load_data(filepath)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' does not exist.")
        sys.exit(1)

    print("Generating Telemetry...")
    plot_telemetry(df)
    
    print("Generating 3D Orbit...")
    plot_orbit_3d(df)

    ani = None
    if args.animate:
        print("Animating the orbits")
        ani = animate_orbit(df)
    
    # Show all plots at once
    plt.show()