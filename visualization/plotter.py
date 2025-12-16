import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config


def load_data(filepath):
    return pd.read_csv(filepath)

def plot_orbit_3d(data, ax=None):
    """
    Accepts data and an optional Matplotlib Axis object.
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
    
    # Plot each satellite
    for name, group in data.groupby('name'):
        ax.plot(group['rx'], group['ry'], group['rz'], label=name)
    
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
    
    # NEW: Groupby loop
    for name, group in data.groupby('name'):
        r_mag = np.sqrt(group['rx']**2 + group['ry']**2 + group['rz']**2)
        alt = (r_mag - config.EARTH_RADIUS) / 1000.0
        v_mag = np.sqrt(group['vx']**2 + group['vy']**2 + group['vz']**2)
        
        ax1.plot(group['time'], alt, label=name)
        ax2.plot(group['time'], v_mag, label=name)
    
    ax1.set_ylabel('Altitude (km)')
    ax1.legend() # Add legend so we know which is which
    ax1.grid(True)
    
    ax2.set_ylabel('Velocity (m/s)')
    ax2.grid(True)
    
    plt.tight_layout()

def animate_orbit(data, save_path=None):
    """
    Animates the trajectory of satellites in 3D.
    """
    # 1. Setup the Figure and 3D Axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 2. Plot Static Earth (Wireframe)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = config.EARTH_RADIUS * np.cos(u) * np.sin(v)
    y = config.EARTH_RADIUS * np.sin(u) * np.sin(v)
    z = config.EARTH_RADIUS * np.cos(v)
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.3)
    
    # 3. Initialize Lines (Trails) and Points (Current Position)
    lines = {}
    points = {}
    
    # Group data by satellite so we can access it easily
    # Dictionary format: {'Sat1': dataframe, 'Sat2': dataframe}
    sat_groups = {name: group for name, group in data.groupby('name')}
    
    # Create empty plot objects for each satellite
    colors = plt.cm.jet(np.linspace(0, 1, len(sat_groups)))
    
    for (name, group), color in zip(sat_groups.items(), colors):
        # Line: The history trail
        line, = ax.plot([], [], [], lw=1, color=color, label=name)
        lines[name] = line
        
        # Point: The current head
        point, = ax.plot([], [], [], marker='o', color=color)
        points[name] = point

    # 4. Set Axis Limits (Crucial! Otherwise the camera jumps around)
    # We find the max extent of ALL data to keep the scale fixed
    max_val = data[['rx', 'ry', 'rz']].abs().max().max()
    limit = max_val * 1.1 # Add 10% buffer
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_title("Orbit Animation")
    ax.legend()
    
    # Add a text element for Time
    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

    # 5. The Update Function (Called every frame)
    # We get unique timestamps to drive the animation
    unique_times = data['time'].unique()
    
    def update(frame_time):
        time_text.set_text(f"Time: {frame_time:.1f} s")
        
        for name, group in sat_groups.items():
            # Get data up to this time (Trail)
            # Optimization: logic can be slow for huge DFs, but fine for MVP
            history = group[group['time'] <= frame_time]
            current = group[group['time'] == frame_time]
            
            if not current.empty:
                # Update Line (History)
                lines[name].set_data(history['rx'], history['ry'])
                lines[name].set_3d_properties(history['rz'])
                
                # Update Point (Head)
                points[name].set_data(current['rx'], current['ry'])
                points[name].set_3d_properties(current['rz'])
                
        return list(lines.values()) + list(points.values()) + [time_text]

    # 6. Create Animation
    # interval=20 means 20ms between frames (50 fps)
    # frames=unique_times[::10] skips every 10th step to speed up playback
    ani = animation.FuncAnimation(
        fig, update, frames=unique_times[::50], interval=20, blit=False
    )
    
    if save_path:
        print(f"Saving animation to {save_path}...")
        ani.save(save_path, writer='pillow', fps=30)
    else:
        return ani

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