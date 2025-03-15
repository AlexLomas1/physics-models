import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class Planet:
    def __init__(self, orbit_radius, orbital_period, marker):
        self.orbit_radius = orbit_radius # In AU
        self.orbital_period = orbital_period # In earth years
        self.angular_velocity = 2 * math.pi / orbital_period 
        self.marker = marker

# Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
Mercury = Planet(0.387, 0.241, None)
Venus = Planet(0.723, 0.615, None)
Earth = Planet(1, 1, None)
Mars = Planet(1.52, 1.88, None)
Jupiter = Planet(5.20, 11.9, None)
Saturn = Planet(9.57, 29.4, None)
Uranus = Planet(19.17, 83.7, None)
Neptune = Planet(30.18, 163.7, None)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

# Setup figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_aspect("equal")
ax.set_facecolor("black")

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=15) 

# Creating markers for the planets
for planet in planets:
    planet.marker, = ax.plot([], [], color="blue", marker="o", markersize=5)

def update(frame_num):
    # Updates Earth's position
    t = frame_num * 0.05  # Used to determine speed of simulation.

    # Parametric equation (r*sin(v*t), r*cos(v*t)), with r and v as constants, used to draw circular orbit.
    for planet in planets:
        x = planet.orbit_radius * math.sin(planet.angular_velocity * t)
        y = planet.orbit_radius * math.cos(planet.angular_velocity * t)
        planet.marker.set_data([x], [y])
    
    return [planet.marker for planet in planets]

# Create animation
# Note: may need to increase number of frames later to allow animation to last longer.
ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

plt.show()