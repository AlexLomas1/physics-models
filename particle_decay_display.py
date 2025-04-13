import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import subprocess
import math
import time

def change_plot(new_val, index):
    global current_data, fig, ax, monte_carlo

    current_data[index] = new_val
    global x_data, y_data
    x_data = [0]
    y_data = [current_data[0]]

    expected_x_data = list(range(0, 51))
    expected_y_data = []
    for x in expected_x_data:
        y = current_data[0] * (math.e)**(-current_data[1]*x)
        expected_y_data.append(y)

    ax.clear()
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()
    time.sleep(0.1)

    display(expected_x_data, expected_y_data)

def display(expected_x_data, expected_y_data):
    global monte_carlo
    monte_carlo = subprocess.Popen(["particle_decay_monte_carlo.exe"], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, text=True)

    monte_carlo.stdin.writelines([(str(current_data[0])+"\n"), str(current_data[1])+"\n", str(current_data[2])+"\n"])
    monte_carlo.stdin.close()

    global graph_line
    graph_line, = ax.plot([], [], label="Random sampling", color="red")

    y_lim = 10 * ((current_data[0] // 10) + 1)
    ax.set_ylim(0, y_lim)
    ax.set_xlim(0, 50)
    expected_line, = ax.plot(expected_x_data, expected_y_data, label="Expected", color="blue", alpha=0.5)

    global ani
    ani = animation.FuncAnimation(fig, update, frames=200, interval=250, blit=False)
    plt.legend(handles=[graph_line, expected_line])
    plt.draw()
    
current_data = [1000, 0.3, 1]

fig, ax = plt.subplots(figsize=(8, 8))

graph_line, = ax.plot([], [], color="red", markersize=1)
x_data = [0]
y_data = [current_data[0]]

text_boxes = []
text_box_data = [
    [plt.axes([0.9, 0.7, 0.05, 0.05]), "N: ", "1000", lambda x: change_plot(float(x), 0)],
    [plt.axes([0.9, 0.6, 0.05, 0.05]), "λ: ", "0.3", lambda x: change_plot(float(x), 1)],
    [plt.axes([0.9, 0.5, 0.05, 0.05]), "dt: ", "1", lambda x: change_plot(float(x), 2)]
]

for box in text_box_data:
    new_text_box = TextBox(box[0], box[1], textalignment="center", initial=box[2])
    new_text_box.on_submit(box[3])
    text_boxes.append(new_text_box)

def update(frame_num):
    global monte_carlo
    particles_remaining = monte_carlo.stdout.readline()
    if not particles_remaining:
        ani.event_source.stop()
        return [graph_line]

    global current_data, x_data, y_data
    x_data.append(x_data[len(x_data)-1] + current_data[2])
    y_data.append(int(particles_remaining))
    graph_line.set_data(x_data, y_data)
    return [graph_line]

expected_x_data = list(range(0, 50))
expected_y_data = []
for x in expected_x_data:
    y = current_data[0] * (math.e)**(-current_data[1]*x)
    expected_y_data.append(y)

display(expected_x_data, expected_y_data)
plt.show()

if monte_carlo:
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()