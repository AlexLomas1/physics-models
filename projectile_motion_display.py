import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import math
import time
import subprocess

class Projectile:
    def __init__(self, label, colour):
        self.label = label
        self.colour = colour

    def set_data(self, h, initial_v, angle, mass, area, drag_coeff):
        self.initial_coordinates = [0, h]
        self.initial_v = initial_v
        self.angle = angle
        self.mass = mass
        self.area = area
        self.drag_coeff = drag_coeff

    def create_marker(self, ax):
        # Creating line to display projectile's path.
        self.marker, = ax.plot([], [], label=self.label, color=self.colour, linestyle="-", linewidth=1)
        # Storing coordinates for projectile's path.
        self.x_values = [self.initial_coordinates[0]]
        self.y_values = [self.initial_coordinates[1]]

Drag = Projectile("Drag", "blue")
NoDrag = Projectile("No Drag", "red")

projectiles = [Drag, NoDrag]

def update_projectile_data(current_data, start):
    global fig, ax, projectiles

    if not start:
        # Closing current animation and subprocess so new animation can be started.
        global ani, projectile_sim
        ani.event_source.stop()
        ax.clear()
        projectile_sim.stdout.close()
        projectile_sim.terminate()
        projectile_sim.wait()
        time.sleep(0.1) # Prevents immediate reopening of orbital engine.
    
    # Updating projectile data
    projectiles[0].set_data(current_data[0], current_data[1], current_data[2], current_data[3],
                            current_data[4], current_data[5])
    projectiles[1].set_data(current_data[0], current_data[1], current_data[2], current_data[3],
                            current_data[4], 0)
    
    display_projectiles(projectiles, fig, ax)

def display_projectiles(projectiles, fig, ax):
    # Setting up figure.
    ax.set_xlabel("x / m")
    ax.set_ylabel("y / m")
    ax.set_aspect("equal")
    ax.grid()
    set_axes_limits(projectiles[0].initial_v, math.radians(projectiles[0].angle),
                    projectiles[0].initial_coordinates[1], ax)
    
    # Opens the compiled dynamics engine as a subprocess.
    global projectile_sim
    projectile_sim = subprocess.Popen(["dynamics_engine.exe"], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True) 
   
    time_step = 0.025
    projectile_sim.stdin.writelines([str(time_step)+"\n"])

    for projectile in projectiles:
        projectile.create_marker(ax)
        data = [str(projectile.initial_coordinates[1]), str(projectile.initial_v), str(projectile.angle), 
                str(projectile.mass), str(projectile.area), str(projectile.drag_coeff)]
        line = " ".join(map(str, data)) + "\n"

        projectile_sim.stdin.writelines([line])
    projectile_sim.stdin.close()

    global ani
    ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)
    plt.legend(handles=[projectile.marker for projectile in projectiles], loc="upper right")

    plt.draw()

def update(frame_num):
    line = projectile_sim.stdout.readline().strip()

    if not line:
        # Stop animation once projectile's motions have both ended
        ani.event_source.stop()
        return [projectile.marker for projectile in projectiles]
    
    values = list(map(float, line.split()))

    for i in range(len(projectiles)):
        x, y = values[2*i], values[(2*i)+1]
        # Only updates position if it has changed (if it hasn't then this projectile's motion has ended)
        if y != projectiles[i].y_values[len(projectiles[i].y_values)-1]:
            projectiles[i].x_values.append(x)
            projectiles[i].y_values.append(y)
            projectiles[i].marker.set_data([projectiles[i].x_values], [projectiles[i].y_values])

    return [projectile.marker for projectile in projectiles]

def set_axes_limits(velocity, angle, h, ax):
    # Calculating max height of non-drag projectile.
    max_h = ((velocity * math.sin(angle))**2 / (2*9.81)) + h
    y_lim = ((max_h // 10) + 1) * 10

    # Calculting final horizontal distance travelled by non-drag projectile.
    temp = velocity * math.sin(angle)
    time = (temp + math.sqrt(temp**2 + 19.62*h)) / 9.81
    max_dist = velocity * math.cos(angle) * time
    x_lim = ((max_dist // 10) + 1) * 10

    ax.set_xlim(0, x_lim)
    ax.set_ylim(0, y_lim)

def change_val(new_val, index):
    global current_data
    current_data[index] = float(new_val)
    update_projectile_data(current_data, start=False)

# Setting up the figure
fig, ax = plt.subplots(figsize=(8, 8))

text_boxes = []
text_boxes_data = [
    [[0.9, 0.8, 0.05, 0.05], "Height: ", "0", lambda x: change_val(x, 0)],
    [[0.9, 0.7, 0.05, 0.05], "Velocity: ", "10", lambda x: change_val(x, 1)],
    [[0.9, 0.6, 0.05, 0.05], "Angle: ", "30", lambda x: change_val(x, 2)],
    [[0.9, 0.5, 0.05, 0.05], "Mass: ", "10", lambda x: change_val(x, 3)],
    [[0.9, 0.4, 0.05, 0.05], "Area: ", "0.5", lambda x: change_val(x, 4)],
    [[0.9, 0.3, 0.05, 0.05], "Drag Coefficient: ", "0.49", lambda x: change_val(x, 5)]
]

# Creating text boxes for data entry
for text_box in text_boxes_data:
    ax_box = plt.axes(text_box[0])
    data_input_box = TextBox(ax_box, text_box[1], textalignment="center", initial=text_box[2])
    data_input_box.on_submit(text_box[3])
    text_boxes.append(data_input_box) # Need to keep a reference to each box for it to remain responsive.

current_data = [0, 10, 30, 10, 0.5, 0.49] # Default data, equivalent to the initial data in text boxes.

update_projectile_data(current_data, start=True)
plt.show()

# Ensures subprocess is closed before ending.
if projectile_sim:
    projectile_sim.stdout.close()
    projectile_sim.terminate()
    projectile_sim.wait()