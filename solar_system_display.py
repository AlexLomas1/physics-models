import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import math
import time
import subprocess

class Planet:
    def __init__(self, name, colour, max_len, diameter, initial_coords, initial_v, mass):
        # Scales planet sizes with a quadratic-logarithmic function.
        self.planet_size = 0.75 * (math.log(diameter, 75))**2
        
        self.name = name
        self.colour = colour
        self.max_len = max_len

        # Data values to be sent to orbital engine
        self.initial_x = initial_coords[0]
        self.initial_y = initial_coords[1]
        self.initial_z = initial_coords[2]
        self.initial_v_x = initial_v[0]
        self.initial_v_y = initial_v[1]
        self.initial_v_z = initial_v[2]
        self.mass = mass * 10**24

    def create_markers(self, ax):
        # Creating planet marker
        self.marker, = ax.plot([], [], [], color=self.colour, marker="o", markersize=self.planet_size, label=self.name)
        # Creating dashed line to display orbital path.
        self.orbit_path, = ax.plot([], [], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path.
        self.x_values = []
        self.y_values = []
        self.z_values = []

# Source for planets' masses, initial coordinates & velocities: https://ssd.jpl.nasa.gov/horizons/app.html
Sun = Planet("Sun", "yellow", 0, 1393000, [-1.068*(10**9), -4.117*(10**8), 3.087*(10**7)], 
            [9.305, -1.283*10, -1.632*(10**-1)], 1988410)
Sun.planet_size = 10 # Manualy setting size of Sun.
Mercury = Planet("Mercury", "grey", 125, 4879, [-2.212*(10**10), -6.682*(10**10), -3.462*(10**9)], 
            [3.666*(10**4), -1.230*(10**4), -4.368*(10**3)], 0.3302)
Venus = Planet("Venus", "khaki", 325, 12104, [-1.086*(10**11), -3.784*(10**9), 6.190*(10**9)], 
            [8.985*(10**2), -3.517*(10**4), -5.320*(10**2)], 4.8685)
Earth = Planet("Earth", "blue", 530, 12756, [-2.628*(10**10), 1.445*(10**11), 0], 
            [-2.983*(10**4), -5.220*(10**3), 0], 5.97219)
Mars = Planet("Mars", "red", 990, 6792, [2.069*(10**11), -3.561*(10**9), 0],
            [1.304*(10**3), 2.628*(10**4), 0], 0.64171)
Jupiter = Planet("Jupiter", "tan", 215, 142984, [5.979*(10**11), 4.387*(10**11), 0],
            [-7.893*(10**3), 1.12*(10**4), 0], 1898.19)
Saturn = Planet("Saturn", "wheat", 515, 120526, [9.576*(10**11), 9.821*(10**11), 0],
            [-7.420*(10**3), 6.726*(10**3), 0], 568.34)
Uranus = Planet("Uranus", "lightblue", 1475, 51118, [2.158*(10**12), -2.055*(10**12), 0],
            [4.647*(10**3), 4.614*(10**3), 0], 86.813)
Neptune = Planet("Neptune", "mediumblue", 2890, 49528, [2.514*(10**12), -3.739*(10**12), 0],
            [4.475*(10**3), 3.063*(10**3), 0], 102.409)

def switch_display(event):
    global orbit_sim, ani, current_display, planets

    if current_display != "Start":
        # Closing current animation and subprocess so new animation can be started.
        ani.event_source.stop()
        ax.clear()
        orbit_sim.stdout.close()
        orbit_sim.terminate()
        orbit_sim.wait()
        time.sleep(0.1) # Prevents immediate reopening of orbital engine.
    else:
        current_display = "Outer" # So inner is displayed next

    if current_display == "Inner":
        current_display = "Outer"
        planets = [Sun, Jupiter, Saturn, Uranus, Neptune]
    else:
        current_display = "Inner"
        planets = [Sun, Mercury, Venus, Earth, Mars]
    
    display_planets(current_display, planets)

def display_planets(current_display, planets):
    global fig, ax, orbit_sim, ani

    # Setting up figure.
    ax.set_aspect("equal")
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.grid()

    # For time steps: this is time step used in calculations by orbital engine, the animation is updated
    # once for every 10 time steps, in order to improve accuracy without making simulation slow.
    if current_display == "Inner":
        ax.set(xlim3d=(-2, 2), xlabel="x / AU")
        ax.set(ylim3d=(-2, 2), ylabel="y / AU")
        ax.set(zlim3d=(-2, 2), zlabel="z / AU")
        time_step = 60 # 1 minute in seconds
        button_label = "Switch to Outer Planets"
    else:
        ax.set(xlim3d=(-35, 35), xlabel="x / AU")
        ax.set(ylim3d=(-35, 35), ylabel="y / AU")
        ax.set(zlim3d=(-35, 35), zlabel="z / AU")
        time_step = 1800 # 30 minutes in seconds
        button_label = "Switch to Inner Planets"
    
    # Runs the compiled orbital engine file as a subprocess.
    orbit_sim = subprocess.Popen(["orbital_engine.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
    # Sending time step to orbital engine.
    orbit_sim.stdin.writelines([(str(time_step)+"\n")])

    # Sending planet masses and initial coordinates and velocities to orbital engine.
    for planet in planets:
        planet.create_markers(ax)
        data = [str(planet.initial_x), str(planet.initial_y), str(planet.initial_z), str(planet.initial_v_x),
                str(planet.initial_v_y), str(planet.initial_v_z), str(planet.mass)]
        line = data[0]+" "+data[1]+" "+data[2]+" "+data[3]+" "+data[4]+" "+data[5]+" "+data[6]+"\n"
        orbit_sim.stdin.writelines([line])
    orbit_sim.stdin.close()

    ani = animation.FuncAnimation(fig, update, frames=1000, interval=50, blit=True)
    plt.legend(title="Planets", handles=[planet.marker for planet in planets[-4:]], bbox_to_anchor=(1.8, 0.05))

    # Changing button label.
    global button
    button.label.set_text(button_label)

    plt.draw()

# frame_num is required for Matplotlib animation, even if it isn't used.
def update(frame_num):
    # Reads a line of output from orbital engine.
    line = orbit_sim.stdout.readline().strip()
    if not line:
        # Stop if no more data.
        return [value for planet in planets for value in [planet.marker, planet.orbit_path]] 
    
    values = list(map(float, line.split()))

    # Updating position of each planet.
    for i in range(len(planets)):
        x, y, z = values[3*i], values[(3*i)+1], values[(3*i)+2]
        planets[i].marker.set_data_3d([x], [y],[z])
        if len(planets[i].x_values) < planets[i].max_len:
            planets[i].x_values.append(x)
            planets[i].y_values.append(y)
            planets[i].z_values.append(z)
            planets[i].orbit_path.set_data_3d(planets[i].x_values,planets[i].y_values,planets[i].z_values)

    return [value for planet in planets for value in [planet.marker, planet.orbit_path]]

# Initialising figure and axes.
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# Creating button to allow for switching between displays.
ax_button = plt.axes([0.4, 0.885, 0.225, 0.05]) 
button = Button(ax_button, "Switch to Outer Planets")
button.on_clicked(switch_display)

current_display = "Start"
switch_display(None)
plt.show()

# Ensures subprocess is closed before ending.
if orbit_sim:
    orbit_sim.stdout.close()
    orbit_sim.terminate()
    orbit_sim.wait()