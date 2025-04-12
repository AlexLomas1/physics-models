import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

monte_carlo = subprocess.Popen(["particle_decay_monte_carlo.exe"], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, text=True)

N = 500

y_lim = 10 * ((N // 10) + 1)
monte_carlo.stdin.writelines(["500\n", "0.3\n"]) # 500 particles, decay constant of 0.3
monte_carlo.stdin.close()

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_ylim(0, y_lim)
ax.set_xlim(0, 50)

graph_line, = plt.plot([], [], color="red", markersize=1)
x_data = [0]
y_data = [N]

def update(frame_num):
    line = monte_carlo.stdout.readline()
    if not line:
        ani.event_source.stop()
        return [graph_line]

    line = int(line)
    x_data.append(x_data[len(x_data)-1] + 1)
    y_data.append(line)
    graph_line.set_data(x_data, y_data)
    return [graph_line]

ani = animation.FuncAnimation(fig, update, frames=200, interval=250, blit=True)

plt.show()

monte_carlo.stdout.close()
monte_carlo.terminate()
monte_carlo.wait()