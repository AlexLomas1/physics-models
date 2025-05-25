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
        # Creating dashed line to display orbital path.
        self.orbit_path, = ax.plot([], [], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path.
        self.x_values, self.y_values, self.z_values = [], [], []

class OrbitSimulation:
    def __init__(self, file_name):
        self.current_display = "Start"
        self.load_data(file_name)
        self.init_plot()
        self.switch_display()
        plt.show()
        self.exit()

    def load_data(self, file_name):
        """Reading data for bodies and storing them as objects in appropriate list."""
        def parse_line(line):
            data = [x.strip() for x in line.split("|") if x.strip() != ""]
            x, y, z, vx, vy, vz, mass = list(map(float, data[5:]))

            if data[1] != "None":
                name, colour, marker_size, trail_len = data[0], data[2], float(data[3]), int(data[4])
                return DisplayedBody(name, colour, marker_size, trail_len, [x, y, z], [vx, vy, vz], mass), data[1]
            else:
                return Body([x, y, z], [vx, vy, vz], mass), "None"

        self.inner = []
        self.outer = []
        self.not_displayed = []

        with open(file_name, "r") as initial_data:
            for line in initial_data:
                if line.startswith("|  # Name") or line.startswith("|:"):
                    continue # Skipping first two lines as they don't contain data

                new_body, display_type = parse_line(line)

                if display_type in ["Inner", "Both"]: 
                    self.inner.append(new_body)
                if display_type in ["Outer", "Both"]: 
                    self.outer.append(new_body)
                elif display_type == "None": 
                    self.not_displayed.append(new_body)
    
    def init_plot(self):
        """Initialising figure and axes, and button for switching between displays"""
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection="3d")

        ax_button = plt.axes([0.4, 0.885, 0.225, 0.05])
        self.button = Button(ax_button, "")
        self.button.on_clicked(self.switch_display)

    def switch_display(self, event=None):
        """Switch between displaying inner and outer planets."""
        if self.current_display != "Start":
            # Closing current animation and subprocess so new animation can be started.
            self.ani.event_source.stop()
            self.ax.clear()
            self.orbital_engine.stdout.close()
            self.orbital_engine.terminate()
            self.orbital_engine.wait()
            time.sleep(0.1) # Prevents immediate reopening of orbital engine.
        
        if self.current_display == "Inner":
            self.current_display = "Outer"
            all_bodies = self.outer + self.inner[1:] + self.not_displayed
            displayed = self.outer
        else: # Inner displayed if current_display is Outer or Start
            self.current_display = "Inner"
            all_bodies = self.inner + self.outer[1:] + self.not_displayed
            displayed = self.inner

        self.display_planets(self.current_display, all_bodies, displayed)

    def display_planets(self, current_display, all_bodies, displayed):
        """Setting up display settings and starting animation."""
        # Setting up axes, and setting panes to black
        self.ax.set_aspect("equal")
        self.ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
        self.ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
        self.ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
        self.ax.grid()
        self.ax.set(xlabel="x / AU", ylabel="y / AU", zlabel="z / AU")

        if current_display == "Inner":
            self.ax.set(xlim3d=(-2, 2), ylim3d=(-2, 2), zlim3d=(-2, 2))
            time_step = 60 # 1 minute in seconds
        else:
            self.ax.set(xlim3d=(-40, 40), ylim3d=(-40, 40), zlim3d=(-40, 40))
            time_step = 7200 # 2 hours in seconds

        self.setup_orbital_engine("orbital_engine.exe", all_bodies, displayed, time_step)

        self.ani = animation.FuncAnimation(self.fig, lambda x: self.update(displayed, x), frames=1000, 
                                           interval=50, blit=True)
        
        # Creating legend, with all displayed bodies except the Sun.
        plt.legend(title="Legend", handles=[body.marker for body in displayed[1:]], bbox_to_anchor=(1.8, 0.05))

        button_label = "Switch to " + ("Inner" if current_display == "Outer" else "Outer") + " Planets"
        self.button.label.set_text(button_label)
    
    def setup_orbital_engine(self, orbit_engine_path, all_bodies, displayed, time_step,):
        """Runs the compiled orbital engine file as a subprocess, and sends the time step and initial
        data for the bodies to the orbital engine."""
        self.orbital_engine = subprocess.Popen([orbit_engine_path], stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, text=True)
    
        self.orbital_engine.stdin.writelines([(str(time_step)+"\n")])

        for body in all_bodies:
            if body in displayed:
                body.create_markers(self.ax)
            data = [str(body.initial_x), str(body.initial_y), str(body.initial_z), str(body.initial_vx),
                str(body.initial_vy), str(body.initial_vz), str(body.mass)]
            line = (" ".join(data)) + "\n"
            self.orbital_engine.stdin.writelines([line])
        self.orbital_engine.stdin.close()

    def update(self, displayed, frame_num):
        """Reads data output from orbital engine and updates the position of each of the displayed bodes."""
        line = self.orbital_engine.stdout.readline().strip()
        if not line: # Stop if no more data.
            return [value for body in displayed for value in [body.marker, body.orbit_path]] 
    
        values = list(map(float, line.split()))

        for i in range(len(displayed)):
            x, y, z = values[3*i], values[(3*i)+1], values[(3*i)+2]
            displayed[i].marker.set_data_3d([x], [y], [z])
            if len(displayed[i].x_values) < displayed[i].trail_len:
                displayed[i].x_values.append(x)
                displayed[i].y_values.append(y)
                displayed[i].z_values.append(z)
                displayed[i].orbit_path.set_data_3d(displayed[i].x_values,displayed[i].y_values,displayed[i].z_values)

        return [value for body in displayed for value in [body.marker, body.orbit_path]]
    
    def exit(self):
        """Ensures subprocess is closed before ending simulation."""
        self.orbital_engine.stdout.close()
        self.orbital_engine.terminate()
        self.orbital_engine.wait()

solar_system_sim = OrbitSimulation("solar_system_data.txt")