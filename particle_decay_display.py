import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import subprocess
import time

def change_plot(new_val, index):
    global current_data, fig, ax, monte_carlo

    current_data[index] = new_val
    global x_data, y_data
    x_data = [0]
    y_data = [current_data[0]]

    ax.clear()
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()
    time.sleep(0.1)

    display()

def display():
    global monte_carlo
    monte_carlo = subprocess.Popen(["particle_decay_monte_carlo.exe"], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, text=True)
    
    y_lim = 10 * ((current_data[0] // 10) + 1)

    monte_carlo.stdin.writelines([(str(current_data[0])+"\n"), str(current_data[1])+"\n"])
    monte_carlo.stdin.close()

    global graph_line
    graph_line, = ax.plot([], [], color="red", markersize=1)

    ax.set_ylim(0, y_lim)
    ax.set_xlim(0, 50)
    global ani
    ani = animation.FuncAnimation(fig, update, frames=200, interval=250, blit=False)
    plt.draw()
    
current_data = [1000, 0.3]

fig, ax = plt.subplots(figsize=(8, 8))

graph_line, = ax.plot([], [], color="red", markersize=1)
x_data = [0]
y_data = [current_data[0]]

ax_N_text_box = plt.axes([0.9, 0.7, 0.05, 0.05])
N_text_box = TextBox(ax_N_text_box, "N: ", textalignment="center", initial="1000")
N_text_box.on_submit(lambda x: change_plot(int(x), 0))

ax_decay_text_box = plt.axes([0.9, 0.6, 0.05, 0.05])
decay_text_box = TextBox(ax_decay_text_box, "Decay constant: ", textalignment="center", initial="0.3")
decay_text_box.on_submit(lambda x: change_plot(float(x), 1))

def update(frame_num):
    global monte_carlo
    particles_remaining = monte_carlo.stdout.readline()
    if not particles_remaining:
        ani.event_source.stop()
        return [graph_line]

    global x_data, y_data
    x_data.append(x_data[len(x_data)-1] + 1)
    y_data.append(int(particles_remaining))
    graph_line.set_data(x_data, y_data)
    return [graph_line]

display()
plt.show()

if monte_carlo:
    monte_carlo.stdout.close()
    monte_carlo.terminate()
    monte_carlo.wait()