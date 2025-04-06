import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
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
        self.marker, = ax.plot([], [], color=self.colour, linestyle="-", linewidth=1)
        # Storing coordinates for projectile's path.
        self.x_values = [self.initial_coordinates[0]]
        self.y_values = [self.initial_coordinates[1]]

# Input data from user
h = input("Height: ")
velocity = input("Velocity: ")
angle = input("Angle: ")
mass = input("Mass: ")
area = input("Area: ")
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
    print(line)

    for i in range(len(projectiles)):
        x, y = values[2*i], values[(2*i)+1]
        # Only updates position if it has changed (if it hasn't then this projectile's motion has ended)
        if y != projectiles[i].y_values[len(projectiles[i].y_values)-1]:
            projectiles[i].x_values.append(x)
            projectiles[i].y_values.append(y)
            projectiles[i].marker.set_data([projectiles[i].x_values], [projectiles[i].y_values])

    return [projectile.marker for projectile in projectiles]

# Setting up the figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel("x / m")
ax.set_xlim(0, 40)
ax.set_ylabel("y / m")
ax.set_ylim(0, 40)
ax.set_aspect("equal")
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
plt.show()

projectile_sim.stdout.close()
projectile_sim.terminate()
projectile_sim.wait()