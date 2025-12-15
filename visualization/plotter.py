# visualization/plots.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import config  # Import your configuration to get EARTH_RADIUS

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_orbit_3d(data, ax=None):
    """
    Accepts data and an optional Matplotlib Axis object.
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
    ax.plot(data['rx'], data['ry'], data['rz'], label='Trajectory', color='b')
    
    # Add a wireframe earth for context
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = config.EARTH_RADIUS * np.cos(u) * np.sin(v)
    y = config.EARTH_RADIUS * np.sin(u) * np.sin(v)
    z = config.EARTH_RADIUS * np.cos(v)
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.3)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.legend()
    
    # Force aspect ratio to be equal so Earth looks spherical
    # (Matplotlib 3D doesn't do this automatically well)
    _set_axes_equal(ax)
    
    return ax

def plot_telemetry(data):
    """
    Creates a 2-panel figure: Altitude and Velocity vs Time.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
    
    # --- 1. Altitude Plot ---
    r_mag = np.sqrt(data['rx']**2 + data['ry']**2 + data['rz']**2)
    alt = (r_mag - config.EARTH_RADIUS) / 1000.0 # Convert to km
    
    ax1.plot(data['time'], alt, color='tab:blue')
    ax1.set_ylabel('Altitude (km)')
    ax1.set_title('Satellite Telemetry')
    ax1.grid(True)
    
    # --- 2. Velocity Plot ---
    v_mag = np.sqrt(data['vx']**2 + data['vy']**2 + data['vz']**2)
    
    ax2.plot(data['time'], v_mag, color='tab:orange')
    ax2.set_ylabel('Velocity Magnitude (m/s)')
    ax2.set_xlabel('Time (s)')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

def _set_axes_equal(ax):
    """
    Helper to force 3D plot to have equal scale on all axes.
    """
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])