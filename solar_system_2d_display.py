import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time
import subprocess

# Setup figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel("x / AU")
ax.set_ylabel("y / AU")
ax.set_aspect("equal")
ax.set_facecolor("black")
ax.grid()

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=25) 

class Planet:
    def __init__(self, name, colour, diameter, semi_major_axis, eccentricity, mass):
        # Scales planet sizes with a quadratic-logarithmic scale (if that is even a thing).
        self.planet_size = 0.75 * (math.log(diameter, 75))**2
        
        self.name = name
        self.colour = colour

        # Storing coordinates for orbital path
        self.x_values = []
        self.y_values = []

        # Data values to be sent to physics engine
        self.semi_major_axis = semi_major_axis * 1.496 * 10**11 # Converting to metres from AU
        self.eccentricity = eccentricity
        self.mass = mass * 10**24 

    def create_markers(self):
        # Creating planet marker
        self.marker, = ax.plot([], [], color=self.colour, marker="o", markersize=self.planet_size, label=self.name)
        # Creating marker for orbital path of planet
        self.orbit_path, = ax.plot([], [], color=self.colour, linestyle="--", linewidth=0.5)

# Note: the colours are just ones I've chosen as I believe they vaguely match images online, and
# are not based on actual scientific facts.
# Source for numerical planet data: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
Mercury = Planet("Mercury", "grey", 4879, 0.387, 0.206, 0.330)
Venus = Planet("Venus", "khaki", 12104, 0.723, 0.007, 4.87)
Earth = Planet("Earth", "blue", 12756, 1.0, 0.017, 5.97)
Mars = Planet("Mars", "red", 6792, 1.523, 0.094, 0.642)
Jupiter = Planet("Jupiter", "tan", 142984, 5.204, 0.049, 1898)
Saturn = Planet("Saturn", "wheat", 120526, 9.583, 0.052, 568)
Uranus = Planet("Uranus", "lightblue", 51118, 19.191, 0.047, 86.8)
Neptune = Planet("Neptune", "mediumblue", 49528, 30.07, 0.010, 102)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

def display_inner_planets():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    # Runs the compiled 2d orbital engine file as a subprocess. 
    global orbit_sim 
    orbit_sim = subprocess.Popen(["orbital_engine_2d.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
    global planets
    planets = [Mercury, Venus, Earth, Mars]

    # Sending time step to orbital engine - 1 day in seconds
    time_step = 86400
    orbit_sim.stdin.writelines([(str(time_step)+"\n")])

    # Writing planetary data to orbital engine
    for planet in planets:
        planet.create_markers()
        data = [str(planet.semi_major_axis), str(planet.eccentricity), str(planet.mass)]
        line = data[0] + " " + data[1] + " " + data[2] + "\n"
        orbit_sim.stdin.writelines([line])
    orbit_sim.stdin.close()

    ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

    plt.legend()
    plt.show()

    # Close the subprocess when done
    orbit_sim.stdout.close()
    orbit_sim.wait()

def display_outer_planets():
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)

    global orbit_sim 
    orbit_sim = subprocess.Popen(["orbital_engine_2d.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
    global planets
    planets = [Jupiter, Saturn, Uranus, Neptune]

    # Sending time step to orbital engine - 20 days in seconds
    time_step = 1728000
    orbit_sim.stdin.writelines([(str(time_step)+"\n")])

    # Writing planetary data to orbital engine
    for planet in planets:
        planet.create_markers()
        data = [str(planet.semi_major_axis), str(planet.eccentricity), str(planet.mass)]
        line = data[0] + " " + data[1] + " " + data[2] + "\n"
        orbit_sim.stdin.writelines([line])
    orbit_sim.stdin.close()

    ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

    plt.legend()
    plt.show()

    # Close the subprocess when done
    orbit_sim.stdout.close()
    orbit_sim.wait()

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
    for i in range(len(planets)):
        x, y = values[2*i], values[(2*i)+1]
        planets[i].x_values.append(x)
        planets[i].y_values.append(y)
        planets[i].orbit_path.set_data(planets[i].x_values,planets[i].y_values)
        planets[i].marker.set_data([x], [y])

    return [value for planet in planets for value in [planet.marker, planet.orbit_path]]

display_inner_planets()

# Delay between running display functions so that orbital engine isn't closed and then immediately 
# reopened. May not actually be necessary.
start = time.time()
while time.time() - start < 1:
    continue

# Need to re-setup the figure after first animation has ended
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel("x / AU")
ax.set_ylabel("y / AU")
ax.set_aspect("equal")
ax.set_facecolor("black")
ax.grid()

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=25) 

display_outer_planets()