import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import subprocess
import math
import time

class ParticleDecaySimulation:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.create_text_boxes()
        self.display(self.current_data)
        plt.show()
        self.exit()
    
    def create_text_boxes(self):
        """Creating text boxes for data entry."""
        self.text_boxes = []
        text_boxes_data = [
            [plt.axes([0.8425, 0.7, 0.05, 0.05]), "N: ", "100", lambda x: self.change_plot(int(x), 0)],
            [plt.axes([0.8425, 0.6, 0.05, 0.05]), "λ (s⁻¹): ", "0.3", lambda x: self.change_plot(float(x), 1)],
            [plt.axes([0.8425, 0.5, 0.05, 0.05]), "dt (s): ", "1", lambda x: self.change_plot(float(x), 2)],
        ]

        for box_data in text_boxes_data:
            new_text_box = TextBox(box_data[0], box_data[1], textalignment="center", initial=box_data[2])
            new_text_box.on_submit(box_data[3])
            self.text_boxes.append(new_text_box) # Need to keep a reference to each box for it to remain responsive.
        
        self.current_data = [100, 0.3, 1] # current_data stores N, λ, dt. These are default values.

    def change_plot(self, new_val, index):
        """Updating data and reseting display settings after data updated by user."""
        self.current_data[index] = new_val

        # Closing current animation and subprocess so new animation can be started.
        if self.ani:
            self.ani.event_source.stop()
        self.ax.clear()
        self.monte_carlo.stdout.close()
        self.monte_carlo.terminate()
        self.monte_carlo.wait()
        time.sleep(0.1) # Prevents immediate reopening of monte carlo program.

        self.display(self.current_data)
    
    def display(self, current_data):
        """Setting up display settings and starting animation."""
        y_lim = 10 * ((current_data[0] // 10) + 1)
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, y_lim)
        self.ax.set(xlabel="t / s", ylabel="N")

        self.x_data = [0]
        self.y_data = [self.current_data[0]]

        self.setup_monte_carlo("ParticlePhysics/particle_decay_monte_carlo.exe", current_data[0], 
                               current_data[1], current_data[2])

        calc_y_values = []
        for x in range(0, 51):
            # Using formula N = N⌄0 * e^(-λt)
            calc_y_values.append(current_data[0] * math.exp(-current_data[1]*x))
    
        calc_line, = self.ax.plot(list(range(0, 51)), calc_y_values, label="Analytical", color="blue", alpha=0.5)
        graph_line, = self.ax.plot([], [], label="Random sampling", color="red")
        
        ani_func = lambda x : self.update(x, graph_line, self.monte_carlo, dt=current_data[2])
        self.ani = animation.FuncAnimation(self.fig, ani_func, frames=200, interval=125, blit=True)
        plt.legend(handles=[graph_line, calc_line], bbox_to_anchor=(1.1, 7.5))

    def setup_monte_carlo(self, monte_carlo_path, N, decay_rate, dt):
        """Runs monte carlo program as a subprocess, and sends the initial data (N, λ, dt)"""
        self.monte_carlo = subprocess.Popen([monte_carlo_path], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, text=True)

        self.monte_carlo.stdin.writelines([str(N)+"\n", str(decay_rate)+"\n", str(dt)+"\n"])
        self.monte_carlo.stdin.close()
    
    def update(self, frame_num, graph_line, monte_carlo, dt):
        """Reads data from monte carlo program and updates the random sampling line."""
        particles_remaining = monte_carlo.stdout.readline()
        if not particles_remaining: # Stop animation once all particles have decayed.
            self.ani.event_source.stop()
            return [graph_line]

        self.x_data.append(self.x_data[len(self.x_data)-1] + dt)
        self.y_data.append(int(particles_remaining))
        graph_line.set_data(self.x_data, self.y_data)
        return [graph_line]
    
    def exit(self):
        """Ensures subprocess is closed before ending simulation."""
        self.monte_carlo.stdout.close()
        self.monte_carlo.terminate()
        self.monte_carlo.wait()

sim = ParticleDecaySimulation()