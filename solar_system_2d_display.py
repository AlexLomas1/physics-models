import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import math
import time
import subprocess

class Planet:
    def __init__(self, name, colour, diameter, semi_major_axis, eccentricity, mass):
        # Scales planet sizes with a quadratic-logarithmic scale (if that is even a thing).
        self.planet_size = 0.75 * (math.log(diameter, 75))**2
        
        self.name = name
        self.colour = colour

        # Data values to be sent to physics engine
        self.semi_major_axis = semi_major_axis * 1.496 * 10**11 # Converting to metres from AU
        self.eccentricity = eccentricity
        self.mass = mass * 10**24 

    def create_markers(self):
        # Creating planet marker
        self.marker, = ax.plot([], [], color=self.colour, marker="o", markersize=self.planet_size, label=self.name)
        # Creating marker for orbital path of planet
        self.orbit_path, = ax.plot([], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path
        self.x_values = []
        self.y_values = []

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

def switch_display(event):
    global orbit_sim, ani, current_display, planets

    if current_display != "Start":
        # Closing the animation and subprocess from previous display
        ani.event_source.stop()
        plt.close()
        orbit_sim.stdout.close()
        orbit_sim.wait()
        time.sleep(0.1) # Prevents immediate reopening of orbital engine after being closed, may be unneeded.
    else:
        current_display = "Outer" # So inner is displayed next

    if current_display == "Inner":
        current_display = "Outer"
        planets = [Jupiter, Saturn, Uranus, Neptune]
    else:
        current_display = "Inner"
        planets = [Mercury, Venus, Earth, Mars]
    display_planets(current_display, planets)

def display_planets(current_display, planets):
    global ax, orbit_sim, ani

    # Setting up figure.
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlabel("x / AU")
    ax.set_ylabel("y / AU")
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.grid()
    ax.plot(0, 0, color="yellow", marker ="o", markersize=25) # Plotting the sun at the centre.

    if current_display == "Inner":
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        time_step = 86400 # 1 day in seconds
        button_label = "Switch to Outer Planets"
    else:
        ax.set_xlim(-35, 35)
        ax.set_ylim(-35, 35)
        time_step = 1728000 # 20 days in seconds
        button_label = "Switch to Inner Planets"
    
    # Runs the compiled 2d orbital engine file as a subprocess
    orbit_sim = subprocess.Popen(["orbital_engine_2d.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
    # Sending time step to orbital engine
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

    # Create button to switch to other display
    global button
    ax_button = plt.axes([0.4, 0.885, 0.225, 0.05]) 
    button = Button(ax_button, button_label)
    button.on_clicked(switch_display)

    plt.show()

# Note that while frame_num isn't used, removing it causes issues with matplotlib for some reason.
def update(frame_num):
    # Reads a line of output from orbital engine.
    line = orbit_sim.stdout.readline().strip()
    if not line:
        # Stop if no more data.
        return [value for planet in planets for value in [planet.marker, planet.orbit_path]] 
    
    values = list(map(float, line.split()))
    
    # Updating position of each planet
    for i in range(len(planets)):
        x, y = values[2*i], values[(2*i)+1]
        planets[i].x_values.append(x)
        planets[i].y_values.append(y)
        planets[i].orbit_path.set_data(planets[i].x_values,planets[i].y_values)
        planets[i].marker.set_data([x], [y])

    return [value for planet in planets for value in [planet.marker, planet.orbit_path]]

current_display = "Start"
switch_display(None)

if orbit_sim:
    orbit_sim.stdout.close()
    orbit_sim.wait()