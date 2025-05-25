import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from matplotlib.widgets import TextBox
import math
import time
import subprocess

class Projectile:
    def __init__(self, label, colour):
        self.label = label
        self.colour = colour
    
    def set_data(self, h, initial_v, angle, mass, area, drag_coeff):
        self.initial_x, self.initial_y = 0, h
        self.initial_v = initial_v
        self.angle = angle
        self.mass = mass
        self.area = area
        self.drag_coeff = drag_coeff

    def create_marker(self, ax):
        # Creating line to display projectile's path.
        self.marker, = ax.plot([], [], label=self.label, color=self.colour, linestyle="-", linewidth=1)
        # Storing coordinates for projectile's path.
        self.x_values = [self.initial_x]
        self.y_values = [self.initial_y]

class ProjectileSimulation:
    def __init__(self):
        Drag = Projectile("Drag", "blue")
        NoDrag = Projectile("No Drag", "red")
        self.projectiles = [Drag, NoDrag]

        self.init_plot()
        self.create_text_boxes()
        self.update_projectile_data(self.current_data, start=True)
        plt.show()
        self.exit()
    
    def init_plot(self):
        """Setting up the figure, and creating two axes to keep text boxes seperate from main axis."""
        self.fig = plt.figure(figsize=(8, 8))
        gs = gridspec.GridSpec(1, 2, width_ratios=[9, 1])
        self.ax = self.fig.add_subplot(gs[0])
        self.ax_input_boxes = self.fig.add_subplot(gs[1])
        self.ax_input_boxes.axis("off")

    def create_text_boxes(self):
        """Creating text boxes for data entry."""
        self.text_boxes = []
        text_boxes_data = [
            [[0.9, 0.7, 0.05, 0.05], "Height (m): ", "0", lambda x: self.change_val(x, 0)],
            [[0.9, 0.6, 0.05, 0.05], "Velocity (m/s): ", "15", lambda x: self.change_val(x, 1)],
            [[0.9, 0.5, 0.05, 0.05], "Angle (°): ", "60", lambda x: self.change_val(x, 2)],
            [[0.9, 0.4, 0.05, 0.05], "Mass (kg): ", "10", lambda x: self.change_val(x, 3)],
            [[0.9, 0.3, 0.05, 0.05], "Area (m²): ", "0.5", lambda x: self.change_val(x, 4)],
            [[0.9, 0.2, 0.05, 0.05], "Drag Coefficient: ", "0.47", lambda x: self.change_val(x, 5)]
        ]

        for box_data in text_boxes_data:
            ax_box = plt.axes(box_data[0])
            new_text_box = TextBox(ax_box, box_data[1], textalignment="center", initial=box_data[2])
            new_text_box.on_submit(box_data[3])
            self.text_boxes.append(new_text_box) # Need to keep a reference to each box for it to remain responsive.

        self.current_data = [0, 15, 60, 10, 0.5, 0.47] # Default data, same as initial data in text boxes.

    def change_val(self, new_val, index):
        self.current_data[index] = float(new_val)
        self.update_projectile_data(self.current_data)
    
    def update_projectile_data(self, current_data, start=False):
        """Update data for projectiles after data is changed by user."""
        if not start:
            # Closing current animation and subprocess so new animation can be started.
            self.ani.event_source.stop()
            self.ax.clear()
            self.projectile_engine.stdout.close()
            self.projectile_engine.terminate()
            self.projectile_engine.wait()
            time.sleep(0.1) # Prevents immediate reopening of dynamics engine.

        # Updating projectile data
        self.projectiles[0].set_data(current_data[0], current_data[1], current_data[2], current_data[3],
                            current_data[4], current_data[5])
        self.projectiles[1].set_data(current_data[0], current_data[1], current_data[2], current_data[3],
                            current_data[4], 0)
        
        self.display_projectiles(self.projectiles)
    
    def display_projectiles(self, projectiles):
        """Setting up display settings and starting animation."""
        self.ax.set(xlabel="x / m", ylabel="y / m")
        self.ax.set_aspect("equal")
        self.ax.grid()
        self.set_axes_limits(projectiles[0].initial_v, math.radians(projectiles[0].angle), projectiles[0].initial_y)

        self.setup_projectile_engine("Mechanics/dynamics_engine.exe", projectiles, time_step=0.025)

        self.ani = animation.FuncAnimation(self.fig, lambda x: self.update(projectiles, x), frames=1000, 
                                           interval=20, blit=True)
        plt.legend(handles=[projectile.marker for projectile in projectiles], loc="center right", bbox_to_anchor=(1.15, 12.7))
    
    def set_axes_limits(self, velocity, angle, h):
        """Sets x and y limits to max height and horizontal distance of non-drag projectile respectively."""
        max_h = ((velocity * math.sin(angle))**2 / (2*9.81)) + h
        y_lim = ((max_h // 10) + 1) * 10

        temp = velocity * math.sin(angle)
        time = (temp + math.sqrt(temp**2 + 19.62*h)) / 9.81
        max_dist = velocity * math.cos(angle) * time
        x_lim = ((max_dist // 10) + 1) * 10

        self.ax.set_xlim(0, x_lim)
        self.ax.set_ylim(0, y_lim)

    def setup_projectile_engine(self, projectile_engine_path, projectiles, time_step):
        """Runs the compiled projectile engine file as a subprocess, and sends the time step and initial
        data for the projectiles to the engine."""
        self.projectile_engine = subprocess.Popen([projectile_engine_path], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True) 
   
        self.projectile_engine.stdin.writelines([str(time_step)+"\n"])

        for projectile in projectiles:
            projectile.create_marker(self.ax)
            data = [str(projectile.initial_y), str(projectile.initial_v), str(projectile.angle), 
                    str(projectile.mass), str(projectile.area), str(projectile.drag_coeff)]
            line = " ".join(map(str, data)) + "\n"
            self.projectile_engine.stdin.writelines([line])
        self.projectile_engine.stdin.close()

    def update(self, projectiles, frame_num):
        """Reads data output from projectile engine and updates the position of each of the projectiles."""
        line = self.projectile_engine.stdout.readline().strip()

        if not line: # Stop animation once both projectiles' motions have ended
            self.ani.event_source.stop()
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
    
    def exit(self):
        """Ensures subprocess is closed before ending simulation."""
        self.projectile_engine.stdout.close()
        self.projectile_engine.terminate()
        self.projectile_engine.wait()

sim = ProjectileSimulation()