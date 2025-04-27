import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import time
import subprocess

class Body:
    def __init__(self, initial_coords, initial_v, mass):
        self.initial_x, self.initial_y, self.initial_z = initial_coords
        self.initial_v_x, self.initial_v_y, self.initial_v_z = initial_v
        self.mass = mass

class DisplayedBody(Body):
    def __init__(self, name, colour, planet_size, max_len, initial_coords, initial_v, mass):
        Body.__init__(self, initial_coords, initial_v, mass)
        self.name = name
        self.colour = colour
        self.planet_size = planet_size
        self.max_len = max_len

    def create_markers(self, ax):
        # Creating planet marker
        self.marker, = ax.plot([], [], [], color=self.colour, marker="o", markersize=self.planet_size, label=self.name)
        # Creating dashed line to display orbital path.
        self.orbit_path, = ax.plot([], [], [], color=self.colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path.
        self.x_values, self.y_values, self.z_values = [], [], []

# Source for masses, initial coordinates & velocities: https://ssd.jpl.nasa.gov/horizons/app.html
Sun = DisplayedBody("Sun", "yellow", 10, 0, [-1.068108951496322e9, -4.177210908491462e8, 3.086887010002915e7], 
            [9.305302656256911, -1.283177282717393e1, -1.631700118015769e-1], 1.98841e30)
Mercury = DisplayedBody("Mercury", "grey", 2, 125, [-2.212073002393702e10, -6.682435921338345e10, -3.461577076477692e9], 
            [3.666229234452722e4, -1.230266984222893e4, -4.368336206255391e3], 3.302e23)
Venus = DisplayedBody("Venus", "khaki", 3.5, 325, [-1.085736592234813e11, -3.784241757371509e9, 6.190088659339075e9], 
            [8.984650886248794e2, -3.517203951420625e4, -5.320225928762774e2], 4.8685e24)
Earth = DisplayedBody("Earth", "blue", 3.6, 530, [-2.627903751048988e10, 1.445101984929515e11, 3.025245352813601e7], 
            [-2.983052803412253e4, -5.220465675237847e3, -1.014855999592612e-1], 5.97219e24)
Moon = Body([-2.659668775178492e10, 1.442683153167126e11, 6.680827660505474e7], 
            [-2.926974096801152e4, -6.020397935372383e3, -1.-1.740818643718001], 7.349e22)
Mars = DisplayedBody("Mars", "red", 3, 990, [2.069269460321208e11, -3.560730804791646e9, -5.147912373388755e9],
            [1.304308855632638e3, 2.628158889664284e4, 5.188465759115868e2], 6.4171e23)
Jupiter = DisplayedBody("Jupiter", "tan", 6, 55, [5.978410555886381e11, 4.387048655696349e11, -1.520164176015472e10],
            [-7.892632213479861e3, 1.115034525890079e4, 1.305100448596264e2], 1.89819e27)
Ganymede = Body([5.968053248329145e11, 4.384332194660895e11, -1.522328734690177e10], 
            [-5.113765418796664e3, 6.421550906276507e2, -2.272690061873600e2], 1.4819e23)
Callisto = Body([5.985070504965953e11, 4.404607314417327e11, -1.513552467401242e10],
            [-1.555591380938867e4, 1.411983421029682e4, 1.260864791234662e2], 1.075938e23)
Io = Body([5.978858478372957e11, 4.382845869031813e11, -1.521589278499892e10],
            [9.292668374291811e3, 1.302536329247139e4, 4.581466304828696e2], 8.9319e22)
Europa = Body([5.972089739395823e11, 4.389225369002028e11, -1.520468461392254e10],
            [-1.226471955004536e4, -1.925433982145555e3, -2.954246238557003e2], 4.79984e22)
Saturn = DisplayedBody("Saturn", "wheat", 5.5, 130, [9.576382282218235e11, 9.821474893679625e11, -5.518978744215649e10],
            [-7.419580377753652e3, 6.725982467906618e3, 1.775011906748625e2], 5.6834e26)
Titan = Body([9.568612740357200e11, 9.830500532492077e11, -5.557945337040257e10],
            [-1.169879722260660e4, 3.942276878869388e3, 2.034192751227804e3], 1.34553e23)
Uranus = DisplayedBody("Uranus", "lightblue", 4.7, 370, [2.157706372184191e12, -2.055243161071827e12, -3.559278015686727e10],
            [4.646952926205451e3, 4.614360059359629e3, -4.301869182469398e1], 8.6813e25)
Neptune = DisplayedBody("Neptune", "blue", 4.7, 725, [2.513785451779509e12, -3.739265135509532e12, 1.907027540535474e10],
            [4.475107938022004e3, 3.062850546988970e3, -1.667293921151841e2], 1.02409e26)
Triton = Body([2.513485337834573e12, -3.739285517961089e12, 1.925835246175838e10],
            [5.751707772788690e3, 6.502827259686770e3, 2.243198849850350e3], 2.1389e22)
Pluto = DisplayedBody("Pluto", "grey", 2, 1095, [-1.478626316093727e12, -4.182878001958115e12, 8.753001980515536e11], 
            [5.271208561199050e3, -2.661768636878488e3, -1.242019729022856e3,], 1.307e22)
Charon = Body([-1.478626356943208e12, -4.182888404805530e12, 8.752835897474382e11], 
            [5.107231584067266e3, -2.789796541800040e3, -1.161460833249591e3], 1.5897e21)

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

    if current_display == "Inner":
        current_display = "Outer"
        bodies = [Sun, Jupiter, Saturn, Uranus, Neptune, Pluto, Mercury, Venus, Earth, Moon, Mars, Ganymede, Callisto, Io, Europa, Titan, Triton, Charon]
        displayed = [Sun, Jupiter, Saturn, Uranus, Neptune, Pluto]
    else: # Inner displayed if switched from outer or simulation just started
        current_display = "Inner"
        bodies = [Sun, Mercury, Venus, Earth, Mars, Moon, Jupiter, Ganymede, Callisto, Io, Europa, Saturn, Titan, Uranus, Neptune, Triton, Pluto, Charon]
        displayed = [Sun, Mercury, Venus, Earth, Mars]
    
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

    # Sending planet masses and initial coordinates and velocities to orbital engine.
    for body in bodies:
        if body in displayed:
            body.create_markers(ax)
        data = [str(body.initial_x), str(body.initial_y), str(body.initial_z), str(body.initial_v_x),
                str(body.initial_v_y), str(body.initial_v_z), str(body.mass)]
        line = data[0]+" "+data[1]+" "+data[2]+" "+data[3]+" "+data[4]+" "+data[5]+" "+data[6]+"\n"
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
        displayed[i].marker.set_data_3d([x], [y],[z])
        if len(displayed[i].x_values) < displayed[i].max_len:
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