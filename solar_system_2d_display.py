import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

# Setup figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-35, 35)
ax.set_xlabel("x / AU")
ax.set_ylim(-35, 35)
ax.set_ylabel("y / AU")
ax.set_aspect("equal")
ax.set_facecolor("black")
ax.grid()

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=15) 

class Planet:
    def __init__(self, name, colour, semi_major_axis, eccentricity, mass):
        self.name = name
        self.colour = colour
        # Creating marker for the planet
        self.marker, = ax.plot([], [], color=colour, marker="o", markersize=5, label=name)
        # Creating orbital path of planet
        self.orbit_path, = ax.plot([], [], color=colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path
        self.x_values = []
        self.y_values = []

        # Data values to be sent to physics engine
        self.semi_major_axis = semi_major_axis * 1.496 * 10**11 # Converting to metres
        self.eccentricity = eccentricity
        self.mass = mass * 10**24 

# Note: the colours are just ones I've chosen as I believe they vaguely match images online, and
# are not based on actual scientific facts.
# Source for semi-major axis, eccentricity, and mass: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
Mercury = Planet("Mercury", "grey", 0.387, 0.206, 0.330)
Venus = Planet("Venus", "khaki", 0.723, 0.007, 4.87)
Earth = Planet("Earth", "blue", 1.0, 0.017, 5.97)
Mars = Planet("Mars", "red", 1.523, 0.094, 0.642)
Jupiter = Planet("Jupiter", "tan", 5.204, 0.049, 1898)
Saturn = Planet("Saturn", "wheat", 9.583, 0.052, 568)
Uranus = Planet("Uranus", "lightblue", 19.191, 0.047, 86.8)
Neptune = Planet("Neptune", "mediumblue", 30.07, 0.010, 102)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

# Runs the compiled 2d orbital engine file as a subprocess. stdin 
orbit_sim = subprocess.Popen(["orbital_engine_2d.exe"], stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, text=True)

# Note that while frame_num isn't used, removing it causes issues with matplotlib for some reason.
def update(frame_num):
    # Reads a line of output from orbital engine.
    line = orbit_sim.stdout.readline().strip()
    if not line:
        # Stop if no more data.
        return [value for planet in planets for value in [planet.marker, planet.orbit_path]] 
    
    values = line.split()
    for i in range(len(values)):
        values[i] = float(values[i])
    
    # Updating position of each planet
    for i in range(8):
        x, y = values[2*i], values[(2*i)+1]
        planets[i].x_values.append(x)
        planets[i].y_values.append(y)
        planets[i].orbit_path.set_data(planets[i].x_values,planets[i].y_values)
        planets[i].marker.set_data([x], [y])

    return [value for planet in planets for value in [planet.marker, planet.orbit_path]]

# Writing planetary data to orbital engine
for planet in planets:
    data = [str(planet.semi_major_axis), str(planet.eccentricity), str(planet.mass)]
    line = data[0] + " " + data[1] + " " + data[2] + "\n"
    orbit_sim.stdin.writelines([line])
orbit_sim.stdin.close()

# Create animation
# Note: may need to increase number of frames later to allow animation to last longer.
ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

plt.legend()
plt.show()

# Close the subprocess when done
orbit_sim.stdout.close()
orbit_sim.wait()