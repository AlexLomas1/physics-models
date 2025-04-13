# Overview
This is a collection of computer models for systems pertaining to various different areas of physics. All models are programmed in C++, and Python programs are used for the purpose of running these models as simulations, visually representing them in real time, and also providing some basic UI elements. For descriptions of specific models, please refer below.

## Table of Contents
- [2D Solar System](#2d-solar-system-model)
- [Particle Decay](#particle-decay-model)
- [Projectile Motion](#projectile-motion-model)

## 2D Solar System Model

https://github.com/user-attachments/assets/bab34c75-d50d-478a-bd48-eba26047a6a7

https://github.com/user-attachments/assets/ef4c7f38-a7b7-4cd3-b75c-be6c7cc8bb0a

Files: `solar_system_2d_display.py`, `orbital_engine_2d.cpp`

This is a simple model that simulates the orbits of the planets in the solar system in two dimensions. The inner planets (Mercury, Venus, Earth, Mars), and the outer planets (Jupiter, Saturn, Uranus, Neptune) are simulated separately as the difference in orbital periods and distances from the sun make it more convenient to plot them using different scales and time steps. Currently no dwarf planets or other non-planetary bodies, excluding the sun, are included in the model.

All of the calculations are performed within `orbital_engine_2d.cpp`. The graphical representation of the model is created within `solar_system_2d_display.py`, which provides the orbital engine with each of the planets’ initial coordinates, initial velocities, and mass, and then plots the planet’s orbits with coordinates output by the orbital engine. The display program also allows for manual switching between the inner planets and outer planet simulations.

The initial coordinates and velocities of each of the planets is taken from the [JPL Horizons System](https://ssd.jpl.nasa.gov/horizons/)'s data for January 1st 2000. The sequential orbits of the planets are then modelled using classical mechanics. 

The gravitational force, $$F$$, exerted on each planet by the Sun is calculated using Newton’s law of universal gravitation:

$$F = G \frac{M m}{r^2}$$

where 
* $$G$$ is the gravitational constant (taken to be $$6.6743 \times 10^{-11} m^3kg^{-1}s^{-2}$$),
* $$M$$ and $$m$$ are the masses of the Sun and the planet respectively, and
* $$r$$ is the distance between them. 

The force is then resolved into $$x$$ and $$y$$ directions, and the accelerations of the planet in these directions is calculated as:

$$a = -\frac{F}{m}$$

The acceleration is negative in order to set the direction of the planet’s acceleration to be towards $$[0, 0]$$, which is the coordinates of the Sun.

The position of the planets are then updated at fixed time steps (2 hours for inner planets, 2 days for outer planets) using velocity verlet integration, which is implemented as follows:

$$x(t+\Delta t) = x(t) + v_x(t) \Delta t + \frac{1}{2} a_x(t) (\Delta t)^2$$ 

$$y(t+\Delta t) = y(t) + v_y(t) \Delta t + \frac{1}{2} a_y(t) (\Delta t)^2$$ 

The values for $$a_x(t+\Delta t)$$ and $$a_y(t+\Delta t)$$ are then calculated, and velocities are updated as: 

$$v_x(t+\Delta t) = v_x(t) + \frac{1}{2} \big(a_x(t) + a_x(t+\Delta t)\big) \Delta t$$ 

$$v_y(t+\Delta t) = v_y(t) + \frac{1}{2} \big(a_y(t) + a_y(t+\Delta t)\big) \Delta t$$

The above process is repeated 10 times for each planet before the planet’s new coordinates are output to be plotted in the simulation. This is done to allow for a shorter time step which drastically increases accuracy, without requiring the simulation to be much slower, or to have a higher frame rate which would make the simulation more memory intensive. 

Currently, all calculated coordinates for each planet remain stored for the entire duration of the simulation for the plotting of the planet’s orbital path. This is done to showcase how much (or little) the planet's orbits deviate over time due to inaccuracies in calculations. However, this can lead to the program becoming very memory intensive if run for a significant amount of time. The code can be quite simply adapted to only store a certain number of previous coordinates, or to not plot the orbital path at all, if this is an issue.

### Limitations

* Currently only the gravitational forces exerted on the planets by the Sun are considered. The gravitational forces of planets acting on other planets, or of planets acting on the Sun, are not considered.
* The model is based purely on classical mechanics, and so relativistic effects are not considered.
* A relatively high time step is used (2 hours for inner planets, 2 days for outer planets), which leads to small inaccuracies that add up over time, and can become an issue if the simulation is run for a significant amount of time. 
* The relative sizes between each of the planets and the sun are not accurately represented, as this would make it difficult to keep all bodies in the simulation visible.

## Particle Decay Model

https://github.com/user-attachments/assets/e1f3163f-52cd-4e29-8e16-31c4a2d88a46

Files: `particle_decay_display.py`, `particle_decay_monte_carlo.cpp`

This model simulates radioactive decay using Monte Carlo methods. This is a method which relies on repeated random sampling to obtain results. The decay is simulated based on two values, both defined by the user at run-time: the original number of particles in a sample, $$N_0$$, and the decay constant, $$\lambda$$. 

First, the analytical solution for the decay is plotted so that it can be compared to the values obtained from random sampling. The rate of decay is proportional to the number of undecayed nuclei, so:

$$\frac{dN}{dt} = -\lambda N$$

We can then rearrange and integrate as follows:

$$\frac{1}{N} \frac{dN}{dt} = -\lambda$$

$$\ln(N) = -\lambda t + c$$

$$N = e^{-\lambda t + c} = ke^{-\lambda t}$$

Where $$c$$ and $$k$$ are constants. As $$N = N_0$$ when $$t = 0$$, we get:

$$N = N_0e^{-\lambda t}$$

For the random sampling, we introduce a third variable: the time step $$\Delta t$$, which is considered to be the time between checks to determine if a particular nuclei has decayed.

The probability of an individual nucleus decaying within the discrete time interval is given as:

$$P = 1 - e^{-\lambda \Delta t}$$

For each undecayed nucleus, a (pseudo) random number is generated between $$0$$ and $$1$$, with a uniform distribution. The value is generated using MT19937, an implementation of the Mersenne Twister algorithm, using the current time as a seed. If this value is less than $$P$$, then the nucleus is considered to have decayed. This process is continued until all of the nuclei have decayed.

## Projectile Motion Model

https://github.com/user-attachments/assets/da028cc4-387d-4034-a39e-0e7faa7da52f

Files: `projectile_motion_display.py`, `dynamics_engine.cpp`

This is a simple model that simulates the motion of a projectile within a uniform gravitational field in two dimensions. The motion of two identical projectiles are simulated concurrently but under different conditions, one with drag and one without, so as to allow comparison between the two.

All of the calculations are performed within `dynamics.cpp`. The graphical representation of the model is created within `projectile_motion_display.py`, which provides the dynamics engine with the projectile's initial height, velocity, and angle of velocity, as well as its area, mass, and drag coefficient (all of which are set by the user at run-time). The projectile for which drag is not considered has its drag coefficient given as $$0$$.

The drag force, $$F$$, exerted on the projectile is calculated as:

$$F = \frac{1}{2} \rho v^2 C_D A$$

where:
* $$\rho$$ is the density of the fluid (in this case the air, taken to be $$1.225kgm^{-3}$$),
* $$v$$ is the velocity of the projectile,
* $$C_D$$ is the drag coefficient, and
* $$A$$ is the cross-sectional area of the projectile.

The force is then resolved into the $$x$$ and $$y$$ directions, and used to calculate the acceleration of the projectile in these directions due to the drag force using $$a=\frac{F}{m}$$. The accelerations are then made to be the opposite sign to the velocity in that direction, and the acceleration due to gravity ($$-9.81ms^{-2}$$) is added to $$a_y$$.

The position of the projectile is then updated at fixed time steps ($$0.025s$$), using velocity verlet integration like with the Solar System model, which is implemented as:

$$x(t+\Delta t) = x(t) + v_x(t) \Delta t + \frac{1}{2} a_x(t) (\Delta t)^2$$ 

$$y(t+\Delta t) = y(t) + v_y(t) \Delta t + \frac{1}{2} a_y(t) (\Delta t)^2$$ 

Values for $$a_x(t+\Delta t)$$ and $$a_y(t+\Delta t)$$ are calculated, and velocities updated as: 

$$v_x(t+\Delta t) = v_x(t) + \frac{1}{2} \big(a_x(t) + a_x(t+\Delta t)\big) \Delta t$$ 

$$v_y(t+\Delta t) = v_y(t) + \frac{1}{2} \big(a_y(t) + a_y(t+\Delta t)\big) \Delta t$$

This continues until the $$y$$ coordinate of the projectile is $$0$$ (so the projectile has hit the ground), after which these final coordinates are output without being updated until both projectiles' motions have ended, at which point the simulation ends.

The point where $$y=0$$ is, of course, unlikely to occur exactly on one of the time steps. For this reason, the previous $$x$$ and $$y$$ values are stored for each projectile, so that when $$y\le0$$, the value of x for which $$y=0$$ can be estimated using linear interpolation:

$$x_{y=0} \approx \frac{x(t)y(t + \Delta t) - x(t + \Delta t)y(t)}{y(t + \Delta t) - y(t)}$$

### Limitations
* This model assumes a drag coefficient and cross-sectional area that are unchanged by orientation, which is a rather large simplification.
* The projectile is treated as a point mass (with the exception of it having a cross-sectional area), so factors such as lift and the moment of inertia are not considered.
* This model assumes a uniform gravitational field and air density. 
* The planet's curvature is not accounted for, making the model unsuitable for very large distance trajectories.
