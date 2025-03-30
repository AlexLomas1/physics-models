import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import math
import time
import subprocess

class Planet:
    def __init__(self, name, colour, diameter, initial_coords, initial_v, mass):
        # Scales planet sizes with a quadratic-logarithmic scale (if that is even a thing).
        self.planet_size = 0.75 * (math.log(diameter, 75))**2
        
        self.name = name
        self.colour = colour

        # Data values to be sent to physics engine
        self.initial_x = initial_coords[0]
        self.initial_y = initial_coords[1]
        self.initial_v_x = initial_v[0]
        self.initial_v_y = initial_v[1]
        self.mass = mass * 10**24

    def create_markers(self, ax):
        # Creating planet marker
        self.marker, = ax.plot([], [], color=self.colour, marker="o", markersize=self.planet_size, label=self.name)
        # Creating marker for orbital path of planet
        self.orbit_path, = ax.plot([], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path
        self.x_values = []
        self.y_values = []

# Source for planets' diameter and mass: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
# Planets' initial coordinates & velocities (2000-01-01 data to 4sf): https://ssd.jpl.nasa.gov/horizons/app.html
Mercury = Planet("Mercury", "grey", 4879, [-2.212*(10**10), -6.682*(10**10)], 
            [3.666*(10**4), -1.230*(10**4)], 0.330)
Venus = Planet("Venus", "khaki", 12104, [-1.086*(10**11), -3.784*(10**9)], 
            [8.985*(10**2), -3.517*(10**4)], 4.87)
Earth = Planet("Earth", "blue", 12756, [-2.628*(10**10), 1.445*(10**11)], 
            [-2.983*(10**4), -5.220*(10**3)], 5.97)
Mars = Planet("Mars", "red", 6792, [2.069*(10**11), -3.561*(10**9)],
            [1.304*(10**3), 2.628*(10**4)], 0.642)
Jupiter = Planet("Jupiter", "tan", 142984, [5.979*(10**11), 4.387*(10**11)],
            [-7.893*(10**3), 1.12*(10**4)], 1898)
Saturn = Planet("Saturn", "wheat", 120526, [9.576*(10**11), 9.821*(10**11)],
            [-7.420*(10**3), 6.726*(10**3)], 568)
Uranus = Planet("Uranus", "lightblue", 51118, [2.158*(10**12), -2.055*(10**12)],
            [4.647*(10**3), 4.614*(10**3)], 86.8)
Neptune = Planet("Neptune", "mediumblue", 49528, [2.514*(10**12), -3.739*(10**12)],
            [4.475*(10**3), 3.063*(10**3)], 102)

def switch_display(event):
    global orbit_sim, ani, current_display, planets

    if current_display != "Start":
        # Closing the animation and subprocess from previous display, and clearing the axes
        ani.event_source.stop()
        ax.clear()
        orbit_sim.stdout.close()
        orbit_sim.terminate()
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
    global fig, ax, orbit_sim, ani

    # Setting up figure.
    ax.set_xlabel("x / AU")
    ax.set_ylabel("y / AU")
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.grid()
    ax.plot(0, 0, color="yellow", marker ="o", markersize=25) # Plotting the sun at the centre.

    # For time steps: smaller steps would increase accuracy, but makes simulation slower as well
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
        planet.create_markers(ax)
        data = [str(planet.initial_x), str(planet.initial_y), str(planet.initial_v_x), 
                str(planet.initial_v_y), str(planet.mass)]
        line = data[0] + " " + data[1] + " " + data[2] + " " + data[3] + " " + data[4] + "\n"
        orbit_sim.stdin.writelines([line])
    orbit_sim.stdin.close()

    ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)
    plt.legend(title="Planets", handles=[planet.marker for planet in planets], bbox_to_anchor=(1.8, 0.05))

    # Create button to switch to other display
    global button
    button.label.set_text(button_label)

    plt.draw()

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

# Initialising figure and axes
fig, ax = plt.subplots(figsize=(8, 8))

# Creating button to allow for switching between displays
ax_button = plt.axes([0.4, 0.885, 0.225, 0.05]) 
button = Button(ax_button, "Switch to Outer Planets")
button.on_clicked(switch_display)

current_display = "Start"
switch_display(None)
plt.show()

# Ensures subprocess is closed before ending
if orbit_sim:
    orbit_sim.stdout.close()
    orbit_sim.terminate()
    orbit_sim.wait()