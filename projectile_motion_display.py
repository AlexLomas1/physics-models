import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import math
import subprocess

class Projectile:
    def __init__(self, label, colour, h, initial_v, angle, mass, area, drag_coeff):
        self.label = label
        self.colour = colour
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

# Input data from user
h = input("Height (m): ")
velocity = input("Velocity (ms^-1): ")
angle = input("Angle: ")
mass = input("Mass (kg): ")
area = input("Area (m^2): ")
drag_coeff = input("Drag coefficient: ")

Drag = Projectile("Drag", "blue", h, velocity, angle, mass, area, drag_coeff)
NoDrag = Projectile("No Drag", "red", h, velocity, angle, mass, area, 0)
projectiles = [Drag, NoDrag]

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

# Setting up the figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel("x / m")
ax.set_ylabel("y / m")
ax.set_aspect("equal")
set_axes_limits(float(velocity), math.radians(float(angle)), float(h), ax)
ax.grid()

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
    line = data[0] + " " + data[1] + " " + data[2] + " " + data[3] + " " + data[4] + " " + data[5] + "\n"

    projectile_sim.stdin.writelines([line])
projectile_sim.stdin.close()

ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

def change_height(new_height):
    print("New height:", new_height)

def change_velocity(new_v):
    print("New velocity:", new_v)

def change_angle(new_angle):
    print("New angle:", new_angle)

def change_mass(new_mass):
    print("New mass:", new_mass)

def change_area(new_area):
    print("New area:", new_area)

def change_drag_coeff(new_drag_coeff):
    print("New drag coefficient:", new_drag_coeff)

ax_height_input = fig.add_axes([0.9, 0.8, 0.05, 0.05])
height_input = TextBox(ax_height_input, "Height: ", textalignment="center")
height_input.on_submit(change_height)

ax_velocity_input = fig.add_axes([0.9, 0.7, 0.05, 0.05])
velocity_input = TextBox(ax_velocity_input, "Velocity: ", textalignment="center")
velocity_input.on_submit(change_velocity)

ax_angle_input = fig.add_axes([0.9, 0.6, 0.05, 0.05])
angle_input = TextBox(ax_angle_input, "Angle: ", textalignment="center")
angle_input.on_submit(change_angle)

ax_mass_input = fig.add_axes([0.9, 0.5, 0.05, 0.05])
mass_input = TextBox(ax_mass_input, "Mass: ", textalignment="center")
mass_input.on_submit(change_mass)

ax_area_input = fig.add_axes([0.9, 0.4, 0.05, 0.05])
area_input = TextBox(ax_area_input, "Area: ", textalignment="center")
area_input.on_submit(change_area)

ax_drag_coeff_input = fig.add_axes([0.9, 0.3, 0.05, 0.05])
drag_coeff_input = TextBox(ax_drag_coeff_input, "Drag coefficient: ", textalignment="center")
drag_coeff_input.on_submit(change_drag_coeff)

plt.legend(handles=[projectile.marker for projectile in projectiles], loc="upper right")
plt.show()

projectile_sim.stdout.close()
projectile_sim.terminate()
projectile_sim.wait()