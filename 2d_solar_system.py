import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Setup figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.set_facecolor("black")

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=15) 

# Creating marker for Earth
earth_marker, = ax.plot([], [], color="blue", marker="o", markersize=5)

earth_velocity = 2 * math.pi # Planet velocity determined by 2πr/orbital period, with r in AU and
# orbital period in (Earth) years. As r and orbital period are both 1 for Earth, v is just 2π. 

def update(frame_num):
    # Updates Earth's position
    t = frame_num * 0.0075  # Used to determine speed of simulation

    # Parametric equation (sin(v*t), cos(v*t)), with v as a constant, used to draw circular orbit
    x = math.sin(earth_velocity * t)
    y = math.cos(earth_velocity * t)
    earth_marker.set_data([x], [y])
    
    return [earth_marker]

# Create animation
ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

plt.show()