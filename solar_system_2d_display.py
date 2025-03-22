import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

# Setup figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-35, 35)
ax.set_xlabel("x / AU")
ax.set_ylim(-35, 35)
ax.set_ylabel("y / AU")
ax.set_aspect("equal")
ax.set_facecolor("black")
ax.grid()

# Plotting the sun at position [0, 0]
ax.plot(0, 0, color="yellow", marker ="o", markersize=15) 

class Planet:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        # Creating marker for the planet
        self.marker, = ax.plot([], [], color=colour, marker="o", markersize=5, label=name)
        # Creating orbital path of planet
        self.orbit_path, = ax.plot([], [], color=colour, linestyle="--", linewidth=0.5)
        # Storing coordinates for orbital path
        self.x_values = []
        self.y_values = []

# Note: the colours are just ones I've chosen as I believe they vaguely match images online, and
# are not based on actual scientific facts.
Mercury = Planet("Mercury", "grey")
Venus = Planet("Venus", "khaki")
Earth = Planet("Earth", "blue")
Mars = Planet("Mars", "red")
Jupiter = Planet("Jupiter", "tan")
Saturn = Planet("Saturn", "wheat")
Uranus = Planet("Uranus", "lightblue")
Neptune = Planet("Neptune", "mediumblue")

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

# Runs the compiled 2d orbital engine file as a subprocess.
orbit_sim = subprocess.Popen(["orbital_engine_2d.exe"], stdout=subprocess.PIPE, text=True)

# Note that while frame_num isn't used, removing it causes issues with matplotlib for some reason.
def update(frame_num):
    # Reads a line of output from orbital engine.
    line = orbit_sim.stdout.readline().strip()
    if not line:
        # Stop if no more data.
        return [value for planet in planets for value in [planet.marker, planet.orbit_path]] 
    
    values = line.split()
    for i in range(len(values)):
        values[i] = float(values[i])
    
    # Updating position of each planet
    for i in range(8):
        x, y = values[2*i], values[(2*i)+1]
        planets[i].x_values.append(x)
        planets[i].y_values.append(y)
        planets[i].orbit_path.set_data(planets[i].x_values,planets[i].y_values)
        planets[i].marker.set_data([x], [y])

    return [value for planet in planets for value in [planet.marker, planet.orbit_path]]

# Create animation
# Note: may need to increase number of frames later to allow animation to last longer.
ani = animation.FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

plt.legend()
plt.show()

# Close the subprocess when done
orbit_sim.stdout.close()
orbit_sim.wait()