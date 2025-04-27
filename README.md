# Overview
This is a collection of computer models for systems pertaining to various different areas of physics. All models are programmed in C++, and Python programs are used for the purpose of running these models as simulations, visually representing them in real time, and also providing some basic UI elements. For descriptions and video demonstrations of specific models, please refer below.

## Table of Contents
- [Solar System](#solar-system-model)
- [Particle Decay](#particle-decay-model)
- [Projectile Motion](#projectile-motion-model)

## Solar System Model

https://github.com/user-attachments/assets/7e47d5ab-f21c-4814-91a8-e47475a50576

https://github.com/user-attachments/assets/8f5d12d4-03df-4bd9-9612-69331c4040a2

Files: `solar_system_display.py`, `orbital_engine.cpp`

This is an N-body simulation that simulates the orbits of the planets in the solar system in three dimensions. The inner planets (Mercury, Venus, Earth, Mars), and the outer planets (Jupiter, Saturn, Uranus, Neptune, and the dwarf planet Pluto) are simulated separately as the difference in orbital periods and distances from the sun make it more convenient to plot them using different scales and time steps. Several non-planetary bodies also have their gravitational effects considered - namely Earth's moon, Jupiter's Galilean moons (Ganymede, Callisto, Io, and Europa), Saturn's moon Titan, Neptune's moon Triton, and Pluto's moon Charon - however they are not included in the visual as their orbits are too small to be seen on the scale of the solar system.

All of the calculations are performed within `orbital_engine.cpp`. The graphical representation of the model is created within `solar_system_display.py`, which provides the orbital engine with each of the planets’ initial coordinates, initial velocities, and mass, and then plots the planet’s orbits with coordinates output by the orbital engine. The display program also allows for manual switching between the inner planets and outer planet simulations.

The initial coordinates and velocities of the Sun and each of the planets is taken from the [JPL Horizons System](https://ssd.jpl.nasa.gov/horizons/)'s data for January 1st 2000. The sequential orbits of these bodies are then modelled using classical mechanics. 

The gravitational force, $$F$$, between two bodies is calculated using Newton’s law of universal gravitation:

$$F = G \frac{m_1 m_2}{r^2}$$

where 
* $$G$$ is the gravitational constant (taken to be $$6.6743 \times 10^{-11} m^3{kg}^{-1}s^{-2}$$),
* $$m_1$$ and $$m_2$$ are the masses of the two bodies, and
* $$r$$ is the distance between them. 

After calculating the force between two bodies, A and B, it is then resolved into $$x$$, $$y$$, and $$z$$ directions by:

$$F_x = F \frac{x_B - x_A}{r}$$

$$F_y = F \frac{y_B - y_A}{r}$$

$$F_z = F \frac{z_B - z_A}{r}$$

This gives the force exerted on body A by B, and the acceleration of A due to B can then be calculated using $$a = \frac{F}{m}$$. Per Newton's third law, the force exerted on B by A is of the same magnitude as that exerted on A by B, but in the opposite direction, so the force values are just multiplied by $$-1$$ when calculating the acceleration of B due to A. This means that the accelerations of two bodies due to each other can be calculated at the same time, and there is no need to calculate the force between the two planets twice.

The position of the bodies are updated with fixed time steps (1 minute for inner planets, 2 hours for outer planets) using velocity verlet integration, which is implemented as follows:

$$x(t+\Delta t) = x(t) + v_x(t) \Delta t + \frac{1}{2} a_x(t) (\Delta t)^2$$ 

$$y(t+\Delta t) = y(t) + v_y(t) \Delta t + \frac{1}{2} a_y(t) (\Delta t)^2$$ 

$$z(t+\Delta t) = z(t) + v_z(t) \Delta t + \frac{1}{2} a_z(t) (\Delta t)^2$$ 

The values for $$a_x(t+\Delta t)$$, $$a_y(t+\Delta t)$$, and $$a_z(t+\Delta t)$$ are then calculated by summing all of the accelerations due to the other bodies, and velocities are updated as: 

$$v_x(t+\Delta t) = v_x(t) + \frac{1}{2} \big(a_x(t) + a_x(t+\Delta t)\big) \Delta t$$ 

$$v_y(t+\Delta t) = v_y(t) + \frac{1}{2} \big(a_y(t) + a_y(t+\Delta t)\big) \Delta t$$

$$v_z(t+\Delta t) = v_z(t) + \frac{1}{2} \big(a_z(t) + a_z(t+\Delta t)\big) \Delta t$$

Note that the new positions for all of the bodies are calculated before any new acceleration values are calculated, as otherwise the bodies accelerations due to another body could be based on that other body's previous position. 

The above process is repeated 1000 times for each body before the body’s new coordinates are output to be plotted in the simulation. This is done to allow for a shorter time step which drastically increases accuracy, without requiring the simulation to be much slower, or to have a higher frame rate which would make the simulation more memory intensive. 

### Accuracy

As this model uses data from the JPL Horizons system for the initial coordinates of the bodies, the accuracy of the simulation can be measured by comparing the simulated coordinates of each of the bodies to data from the Horizons system after a certain amount of time. In this case, the model uses the data from January 1st 2000 as its initial data, and then compares the calculated coordinates after 25 years of simulated time to data from January 1st 2025.

The percentage error is calculated by finding the magnitude of the error (the distance between the calculated coordinates and the coordinates from the Horizons system), and dividing this by the magnitude of the Horizons position (i.e., the distance from $$[0, 0, 0]$$):

$$ \text{Percentage error} = \sqrt{\frac{(x_{\text{sim}} - x_{\text{horizons}})^2 + (y_{\text{sim}} - y_{\text{horizons}})^2 + (z_{\text{sim}} - z_{\text{horizons}})^2}{(x_{\text{horizons}})^2 + (y_{\text{horizons}})^2 + (z_{\text{horizons}})^2}} \times 100 \\% $$

The table below shows the percentage errors, to six significant figures, for each planet (and the dwarf planet Pluto) for different time steps:

<table>
  <tr>
    <th rowspan="2">Planets</th>
    <th colspan="3">Percentage error with time step:</th>
  </tr>
  <tr>
    <td align="center"> <b> 1 minute </b> </td>
    <td align="center"> <b> 2 hours </b> </td>
    <td align="center"> <b> 24 hours </b> </td>
  </tr>
  <tr>
    <td align="center"> Mercury </td>
    <td align="center"> $$0.00770326$$% </td>
    <td align="center"> $$0.629615$$% </td>
    <td align="center"> $$88.2137$$% </td>
  </tr>
  <tr>
    <td align="center"> Venus </td>
    <td align="center"> $$0.00597191$$% </td>
    <td align="center"> $$0.0414255$$% </td>
    <td align="center"> $$6.81998$$% </td>
  </tr>
  <tr>
    <td align="center"> Earth </td>
    <td align="center"> $$0.00742136$$% </td>
    <td align="center"> $$0.00466923$$% </td>
    <td align="center"> $$1.62908$$% </td>
  </tr>
  <tr>
    <td align="center"> Mars </td>
    <td align="center"> $$0.00153313$$% </td>
    <td align="center"> $$0.000503363$$% </td>
    <td align="center"> $$0.276678$$% </td>
  </tr>
  <tr>
    <td align="center"> Jupiter </td>
    <td align="center"> $$0.000425726$$% </td>
    <td align="center"> $$0.000415059$$% </td>
    <td align="center"> $$0.228134$$% </td>
  </tr>
  <tr>
    <td align="center"> Saturn </td>
    <td align="center"> $$0.0084570$$% </td>
    <td align="center"> $$0.00843870$$% </td>
    <td align="center"> $$0.00756711$$% </td>
  </tr>
  <tr>
    <td align="center"> Uranus </td>
    <td align="center"> $$0.00806538$$% </td>
    <td align="center"> $$0.00843870$$% </td>
    <td align="center"> $$0.00808057$$% </td>
  </tr>
  <tr>
    <td align="center"> Neptune </td>
    <td align="center"> $$0.0000435835$$% </td>
    <td align="center"> $$0.0000427924$$% </td>
    <td align="center"> $$0.0190927$$% </td>
  </tr>
  <tr>
    <td align="center"> Pluto </td>
    <td align="center"> $$0.00114799$$% </td>
    <td align="center"> $$0.00119511$$% </td>
    <td align="center"> $$0.00118475$$% </td>
  </tr>
</table>

Note that the 1 minute time step is the one used for simulating the inner planets (Mercury, Venus, Earth, and Mars), and 2 hours is used for the outer bodies. The 24 hour time step is added just for comparison.

A point of interest with these results is how the error for a planet doesn't necessarily decrease as the time step is decreased, contrary to what one may expect. The likely culprit for this is floating-point error - rounding errors due to the finite precision of floating-point operations, which accumulate as more calculations are performed. 

Earth, for instance, has a greater accuracy with a time step of 2 hours than with a time step of 1 minute. Earth's orbit has a fairly small eccentricity, and so its accuracy is not affected significantly by changes to the time step when it is already sufficiently small. What decreasing the time steps does do, however, is vastly increase the number of calculations that are performed, therefore increasing the error due to floating-point errors and giving the counterintuitive result of the accuracy decreasing with a smaller time step.

This effect is also seen, although to a lesser degree, in some of the outer planets such as Saturn and Neptune. Whilst they are both similarly not overly affected by further decreases to the time step, their greater distance from the Sun reduces the impact of these floating-point errors.

Mercury and Venus are the only planets which consistently give an increase in accuracy as the time step is decreased. This is because both have very short orbital periods - Mercury, for example, has an orbital period of only 88 Earth days. This means that they still do experience a noticeable increase in accuracy as the time step is decreased further (especially so for Mercury), enough that this overcomes the increase in floating-point errors, at least within this time period.

### Limitations

* While a fairly low time step is used (1 minute for inner planets, 2 hours for outer planets), this will still lead to small inaccuracies that add up over time, and can become an issue if the simulation is run for a significant amount of time.
* Relativistic effects have not been considered.
* The relative sizes between each of the planets and the sun are not accurately represented, nor the distances between them, as this would make it difficult to keep all bodies in the simulation visible.
* Only a limited number of bodies within the solar system have had their gravitational effects considered.

## Particle Decay Model

https://github.com/user-attachments/assets/e1f3163f-52cd-4e29-8e16-31c4a2d88a46

Files: `particle_decay_display.py`, `particle_decay_monte_carlo.cpp`

This model simulates radioactive decay using a Monte Carlo approach. This is a method which relies on repeated random sampling to obtain results. The decay is simulated based on two values, both defined by the user at run-time: the original number of particles in a sample, $$N_0$$, and the decay constant, $$\lambda$$. 

First, the analytical solution for the decay is plotted so that it can be compared to the values obtained from random sampling. The rate of decay is proportional to the number of undecayed nuclei, so:

$$\frac{dN}{dt} = -\lambda N$$

We can then rearrange and integrate as follows:

$$\frac{1}{N} \frac{dN}{dt} = -\lambda$$

$$\ln(N) = -\lambda t + c$$

$$N = e^{-\lambda t + c} = ke^{-\lambda t}$$

Where $$c$$ and $$k$$ are constants. As $$N = N_0$$ when $$t = 0$$, we get:

$$N = N_0e^{-\lambda t}$$

For the random sampling, we introduce a third variable: the time step $$\Delta t$$, also user-defined at run-time, which is considered to be the time between checks to determine if a particular nucleus has decayed.

The probability of an individual nucleus decaying within the discrete time interval is:

$$P = 1 - e^{-\lambda \Delta t}$$

For each undecayed nucleus, a (pseudo) random number is generated between $$0$$ and $$1$$, with a uniform distribution. The value is generated using MT19937, an implementation of the Mersenne Twister algorithm based on the Mersenne prime $$2^{19937}-1$$, with the current system time as the seed. If this value is less than $$P$$, then the nucleus is considered to have decayed. This process is continued until all of the nuclei have decayed.

## Projectile Motion Model

https://github.com/user-attachments/assets/da028cc4-387d-4034-a39e-0e7faa7da52f

Files: `projectile_motion_display.py`, `dynamics_engine.cpp`

This is a simple model that simulates the motion of a projectile within a uniform gravitational field in two dimensions. The motion of two identical projectiles are simulated concurrently but under different conditions, one with drag and one without, so as to allow comparison between the two.

All of the calculations are performed within `dynamics.cpp`. The graphical representation of the model is created within `projectile_motion_display.py`, which provides the dynamics engine with the projectile's initial height, velocity, and angle of velocity, as well as its area, mass, and drag coefficient (all of which are set by the user at run-time). The projectile for which drag is not considered has its drag coefficient given as $$0$$.

The drag force, $$F$$, exerted on the projectile is calculated as:

$$F = \frac{1}{2} \rho v^2 C_D A$$

where:
* $$\rho$$ is the density of the fluid (air, taken to be $$1.225kgm^{-3}$$),
* $$v$$ is the velocity of the projectile,
* $$C_D$$ is the drag coefficient, and
* $$A$$ is the cross-sectional area of the projectile.

The force is then resolved into $$x$$ and $$y$$ components, and the acceleration of the projectile in these directions due to the drag force is calculated using Newton's second law, $$a=\frac{F}{m}$$. The accelerations are then made to be the opposite direction to the velocity, and the acceleration due to gravity (taken to be $$-9.81ms^{-2}$$) is added to the vertical acceleration $$a_y$$.

The position of the projectile is then updated at fixed time steps ($$0.025s$$) using velocity verlet integration, like with the Solar System model:

$$x(t+\Delta t) = x(t) + v_x(t) \Delta t + \frac{1}{2} a_x(t) (\Delta t)^2$$ 

$$y(t+\Delta t) = y(t) + v_y(t) \Delta t + \frac{1}{2} a_y(t) (\Delta t)^2$$ 

Values for $$a_x(t+\Delta t)$$ and $$a_y(t+\Delta t)$$ are calculated, and velocities updated as: 

$$v_x(t+\Delta t) = v_x(t) + \frac{1}{2} \big(a_x(t) + a_x(t+\Delta t)\big) \Delta t$$ 

$$v_y(t+\Delta t) = v_y(t) + \frac{1}{2} \big(a_y(t) + a_y(t+\Delta t)\big) \Delta t$$

This continues until the $$y$$ coordinate of the projectile is $$0$$ (so the projectile has hit the ground), after which these final coordinates are output without being updated until both projectiles' motions have ended, at which point the simulation ends.

The point where $$y=0$$ is, of course, unlikely to occur exactly on one of the time steps. For this reason, the previous $$x$$ and $$y$$ values are stored for each projectile, so that when $$y\le0$$, the value of x for which $$y=0$$ can be estimated using linear interpolation:

$$x_{y=0} \approx \frac{x(t)y(t + \Delta t) - x(t + \Delta t)y(t)}{y(t + \Delta t) - y(t)}$$

### Limitations
* This model assumes a drag coefficient and cross-sectional area that do not change with orientation, which is a rather large simplification.
* The projectile is treated as a point mass, with the exception of it having a cross-sectional area. As a result, factors such as lift and the rotational dynamics are not considered.
* This model assumes a uniform gravitational field and air density. 
* The planet's curvature is not accounted for, making the model unsuitable for trajectories that span very large distance.
