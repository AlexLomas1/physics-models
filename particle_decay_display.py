import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import subprocess
import math
import time

def update(frame_num, graph_line, monte_carlo, dt):
    particles_remaining = monte_carlo.stdout.readline()
    if not particles_remaining:
        # Stop animation once all particles have decayed.
        ani.event_source.stop()
        return [graph_line]

    global x_data, y_data
    x_data.append(x_data[len(x_data)-1] + dt)
    y_data.append(int(particles_remaining))
    graph_line.set_data(x_data, y_data)
    return [graph_line]

def display():
    global monte_carlo
    monte_carlo = subprocess.Popen(["particle_decay_monte_carlo.exe"], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, text=True)

    monte_carlo.stdin.writelines([(str(current_data[0])+"\n"), str(current_data[1])+"\n", str(current_data[2])+"\n"])
    monte_carlo.stdin.close()

    graph_line, = ax.plot([], [], label="Random sampling", color="red")

    calc_y_values = []
    for x in range(0, 51):
        # Using formula N = N⌄0 * e^(-λt)
        calc_y_values.append(current_data[0] * math.exp(-current_data[1]*x))
    
    analytical_line, = ax.plot(list(range(0, 51)), calc_y_values, label="Analytical", color="blue", alpha=0.5)

    y_lim = 10 * ((current_data[0] // 10) + 1)
    ax.set_xlim(0, 50)
    ax.set_xlabel("t / s")
    ax.set_ylim(0, y_lim)
    ax.set_ylabel("N")

    global ani
    ani_func = lambda x : update(x, graph_line, monte_carlo, dt=current_data[2])
    ani = animation.FuncAnimation(fig, ani_func, frames=200, interval=125, blit=True)
    plt.legend(handles=[graph_line, analytical_line], bbox_to_anchor=(1.1, 7.5))
    plt.draw()

def change_plot(new_val, index):
    global current_data, x_data, y_data, ax, monte_carlo

    current_data[index] = new_val
    x_data = [0]
    y_data = [current_data[0]]

    # Clearing axis and closing subprocess so the new animation can start.
    ax.clear()
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()
    time.sleep(0.1) # Prevents immediate reopening of monte carlo program.

    display()

current_data = [100, 0.3, 1] # current_data stores N, λ, dt. These are default values.

fig, ax = plt.subplots(figsize=(8, 8))

x_data = [0]
y_data = [current_data[0]]

# Creating text boxes for data entry.
text_boxes = []
text_boxes_data = [
    [plt.axes([0.8425, 0.7, 0.05, 0.05]), "N: ", "100", lambda x: change_plot(int(x), 0)],
    [plt.axes([0.8425, 0.6, 0.05, 0.05]), "λ: ", "0.3", lambda x: change_plot(float(x), 1)],
    [plt.axes([0.8425, 0.5, 0.05, 0.05]), "dt: ", "1", lambda x: change_plot(float(x), 2)],
]

for box in text_boxes_data:
    new_text_box = TextBox(box[0], box[1], textalignment="center", initial=box[2])
    new_text_box.on_submit(box[3])
    text_boxes.append(new_text_box)

display()
plt.show()

if monte_carlo:
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()