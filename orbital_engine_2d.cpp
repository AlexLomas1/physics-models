#include <iostream>
#include <cmath>

#define pi 3.14159265358979323846 

/* Note that while this is called orbital_engine, currently it is little more than a fancy circle 
drawer. This is done to test that frontend and the communication between the ends work as intented. */

class Planet {
    public:
        float x;
        float y;
        float orbit_radius;
        float angular_v;
};

int main() {
    Planet planets[8]; // array to store Planet objects.

    // Angular v calculated as 2*pi/orbital_period
    Planet Mercury;
    Mercury.orbit_radius = 0.387;
    Mercury.angular_v = 2 * pi / 0.241;
    planets[0] = Mercury;

    Planet Venus;
    Venus.orbit_radius = 0.723;
    Venus.angular_v = 2 * pi / 0.615;
    planets[1] = Venus;
    
    Planet Earth;
    Earth.orbit_radius = 1;
    Earth.angular_v = 2 * pi;
    planets[2] = Earth;

    Planet Mars;
    Mars.orbit_radius = 1.52;
    Mars.angular_v = 2 * pi / 1.88;
    planets[3] = Mars;

    Planet Jupiter;
    Jupiter.orbit_radius = 5.20;
    Jupiter.angular_v = 2 * pi / 11.9;
    planets[4] = Jupiter;

    Planet Saturn;
    Saturn.orbit_radius = 9.57;
    Saturn.angular_v = 2 * pi / 29.4;
    planets[5] = Saturn;

    Planet Uranus;
    Uranus.orbit_radius = 19.17;
    Uranus.angular_v = 2 * pi / 83.7;
    planets[6] = Uranus;

    Planet Neptune;
    Neptune.orbit_radius = 30.18;
    Neptune.angular_v = 2 * pi / 163.7;
    planets[7] = Neptune;
    
    // May need to increase range of t to allow animation to last longer
    for (int t=0; t <= 1000; t++) {
        for (int i=0; i < 8; i++) {
            // Parametric equation used to find new position of each planet.
            planets[i].x = planets[i].orbit_radius * sin(planets[i].angular_v * t/(5*pi));
            planets[i].y = planets[i].orbit_radius * cos(planets[i].angular_v * t/(5*pi));
            
            // Print new coordinates so Python file can read them.
            std::cout << planets[i].x << " " << planets[i].y;
            // Ensures each coordinate is seperated by a space, but that last coordinate doesn't have
            // a trailing space.
            if (i != 8) {
                std::cout << " ";
            } 
        }
        std::cout << std::endl; // Ends the output line.
    }
}