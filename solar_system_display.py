import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import time
import subprocess

class Body:
    def __init__(self, initial_coords, initial_v, mass):
        self.initial_x, self.initial_y, self.initial_z = initial_coords
        self.initial_vx, self.initial_vy, self.initial_vz = initial_v
        self.mass = mass

class DisplayedBody(Body):
    def __init__(self, name, colour, marker_size, trail_len, initial_coords, initial_v, mass):
        Body.__init__(self, initial_coords, initial_v, mass)
        self.name = name
        self.colour = colour
        self.marker_size = marker_size
        self.trail_len = trail_len

    def create_markers(self, ax):
        # Creating planet marker
        self.marker, = ax.plot([], [], [], color=self.colour, marker="o", markersize=self.marker_size, label=self.name)
        # Creating dashed line to display orbital path trail.
        self.orbit_path, = ax.plot([], [], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path.
        self.x_values, self.y_values, self.z_values = [], [], []

inner = []
outer = []
not_displayed = []

with open("solar_system_data.txt", "r") as initial_data:
    for line in initial_data:
        if line.startswith("|  # Name") or line.startswith("|:"):
            continue # Skipping first two lines

        data = [x.strip() for x in line.split("|") if x.strip() != ""]

        name = data[0]
        x, y, z = list(map(float, data[5:8]))
        vx, vy, vz = list(map(float, data[8:11]))
        mass = float(data[11])

        if data[1] != "None":
            colour, marker_size, trail_len = data[2], float(data[3]), int(data[4])
            new_body = DisplayedBody(name, colour, marker_size, trail_len, [x, y, z], [vx, vy, vz], mass)

            if data[1] == "Inner" or data[1] == "Both":
                inner.append(new_body)
            if data[1] == "Outer" or data[1] == "Both":
                outer.append(new_body)
        else:
            new_body = Body([x, y, z], [vx, vy, vz], mass)
            not_displayed.append(new_body)

def switch_display(event):
    global orbit_sim, ani, current_display

    if current_display != "Start":
        # Closing current animation and subprocess so new animation can be started.
        ani.event_source.stop()
        ax.clear()
        orbit_sim.stdout.close()
        orbit_sim.terminate()
        orbit_sim.wait()
        time.sleep(0.1) # Prevents immediate reopening of orbital engine.

    global inner, outer, not_displayed
    if current_display == "Inner":
        current_display = "Outer"
        bodies = outer + inner[1:len(inner)] + not_displayed
        displayed = outer
    else: # Inner displayed if switched from outer or simulation just started
        current_display = "Inner"
        bodies = inner + outer[1:len(inner)] + not_displayed
        displayed = inner
    
    display_planets(current_display, bodies, displayed)

def display_planets(current_display, bodies, displayed):
    global fig, ax, orbit_sim, ani

    # Setting up axes, and setting panes to black
    ax.set_aspect("equal")
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.grid()

    # For time steps: this is time step used in calculations by orbital engine, the animation is updated
    # once for every 10 time steps, in order to improve accuracy without making simulation slow.
    ax.set(xlabel="x / AU", ylabel="y / AU", zlabel="z / AU")
    if current_display == "Inner":
        ax.set(xlim3d=(-2, 2), ylim3d=(-2, 2), zlim3d=(-2, 2))
        time_step = 60 # 1 minute in seconds
        button_label = "Switch to Outer Planets"
    else:
        ax.set(xlim3d=(-40, 40), ylim3d=(-40, 40), zlim3d=(-40, 40))
        time_step = 7200 # 2 hours in seconds
        button_label = "Switch to Inner Planets"
    
    # Runs the compiled orbital engine file as a subprocess.
    orbit_sim = subprocess.Popen(["orbital_engine.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
    # Sending time step to orbital engine.
    orbit_sim.stdin.writelines([(str(time_step)+"\n")])

    # Sending masses, initial coordinates, and initial velocities to orbital engine.
    for body in bodies:
        if body in displayed:
            body.create_markers(ax)
        data = [str(body.initial_x), str(body.initial_y), str(body.initial_z), str(body.initial_vx),
                str(body.initial_vy), str(body.initial_vz), str(body.mass)]
        line = (" ".join(data)) + "\n"
        orbit_sim.stdin.writelines([line])
    orbit_sim.stdin.close()

    ani = animation.FuncAnimation(fig, lambda x: update(displayed, x), frames=1000, interval=50, blit=True)
    plt.legend(title="Legend", handles=[body.marker for body in displayed[1:]], bbox_to_anchor=(1.8, 0.05))

    # Changing button label.
    global button
    button.label.set_text(button_label)

    plt.draw()

# frame_num is required for Matplotlib animation, even if it isn't used.
def update(displayed, frame_num):
    # Reads a line of output from orbital engine.
    line = orbit_sim.stdout.readline().strip()
    if not line:
        # Stop if no more data.
        return [value for body in displayed for value in [body.marker, body.orbit_path]] 
    
    values = list(map(float, line.split()))

    # Updating position of each planet.
    for i in range(len(displayed)):
        x, y, z = values[3*i], values[(3*i)+1], values[(3*i)+2]
        displayed[i].marker.set_data_3d([x], [y], [z])
        if len(displayed[i].x_values) < displayed[i].trail_len:
            displayed[i].x_values.append(x)
            displayed[i].y_values.append(y)
            displayed[i].z_values.append(z)
            displayed[i].orbit_path.set_data_3d(displayed[i].x_values,displayed[i].y_values,displayed[i].z_values)

    return [value for body in displayed for value in [body.marker, body.orbit_path]]

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