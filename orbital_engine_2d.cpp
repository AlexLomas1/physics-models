#include <iostream>
#include <cmath>

const float pi = 3.14159265358979323846;
const float AU = 1.496 * pow(10,11); // Astronomical Unit in metres
const float G = 6.6743 * pow(10,-11); // Gravitational constant
const float SunMass = 1.989 * pow(10,30); // Mass of sun in kg

class Planet {
    public:
        float x; //  Current x-coordinate (m)
        float y; // Current y-coordinate (m)
        float v_x; // Current velocity in x-direction (ms^-1)
        float v_y; // Current velocity in y-direction (ms^-1)
        float mass; // (kg)
};

void calc_acceleration(float m, float x, float y, float&a_x, float&a_y) {
    /* Force calculted using Newton's law of universal gravitation, with formula F = G * m1 * m2 / (r^2)
    where m1 and m2 are the masses of the two bodies and r is the distance between them. As the sun
    is fixed at [0, 0], the distance is just sqrt(x^2+y^2). */
    float dist_squared = (x*x)+(y*y);
    float dist = sqrt(dist_squared);

    float F = G * m * SunMass / dist_squared;

    // Force resolved into x and y directions using ratios. 
    float F_x = F * x / dist;
    float F_y = F * y / dist;

    // Acceleration calculated using Newton's second law of motion, F = ma. It is negative as planet is
    // being accelerated towards the sun.
    a_x = -F_x / m;
    a_y = -F_y / m;
}

int main() {
    Planet planets[8]; // array to store Planet objects.

    // Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
    Planet Mercury;
    Mercury.y = 0.387 * AU;
    Mercury.x = 0;
    Mercury.v_x = 47400;
    Mercury.v_y = 0;
    Mercury.mass = 0.330 * pow(10,24);
    planets[0] = Mercury;

    Planet Venus;
    Venus.x = 0;
    Venus.y = 0.723 * AU;
    Venus.v_x = 35000;
    Venus.v_y = 0;
    Venus.mass = 4.87 * pow(10,24);
    planets[1] = Venus;
    
    Planet Earth;
    Earth.x = 0;
    Earth.y = 1 * AU;
    Earth.v_x = 29800;
    Earth.v_y = 0;
    Earth.mass = 5.97 * pow(10,24);
    planets[2] = Earth;

    Planet Mars;
    Mars.x = 0;
    Mars.y = 1.52 * AU;
    Mars.v_x = 24100;
    Mars.v_y = 0;
    Mars.mass = 0.642 * pow(10,24);
    planets[3] = Mars;

    Planet Jupiter;
    Jupiter.x = 0;
    Jupiter.y = 5.20 * AU;
    Jupiter.v_x = 13100;
    Jupiter.v_y = 0;
    Jupiter.mass = 1898 * pow(10,24);
    planets[4] = Jupiter;

    Planet Saturn;
    Saturn.x = 0;
    Saturn.y = 9.57 * AU;
    Saturn.v_x = 9700;
    Saturn.v_y = 0;
    Saturn.mass = 568 * pow(10,24);
    planets[5] = Saturn;

    Planet Uranus;
    Uranus.x = 0;
    Uranus.y = 19.17 * AU;
    Uranus.v_x = 6800;
    Uranus.v_y = 0;
    Uranus.mass = 86.8 * pow(10,24);
    planets[6] = Uranus;

    Planet Neptune;
    Neptune.x = 0;
    Neptune.y = 30.18 * AU;
    Neptune.v_x = 5400;
    Neptune.v_y = 0;
    Neptune.mass = 102 * pow(10,24);
    planets[7] = Neptune;
    
    // May need to increase range of t to allow animation to last longer.
    for (int t=0; t <= 1000; t++) {
        for (int i=0; i < 8; i++) {
            float a_x, a_y;
            calc_acceleration(planets[i].mass, planets[i].x, planets[i].y, a_x, a_y);
            // a_x and a_y passed by reference.

            planets[i].v_x += a_x * 864000; // 10 days in seconds
            planets[i].v_y += a_y * 864000;

            planets[i].x += planets[i].v_x * 864000;
            planets[i].y += planets[i].v_y * 864000;
            
            // Converts coordinates to AU and prints them so Python file can read them.
            std::cout << planets[i].x/AU << " " << planets[i].y/AU;
            // Ensures each coordinate is seperated by a space, but that last coordinate doesn't have
            // a trailing space.
            if (i != 7) {
                std::cout << " ";
            } 
        }
        std::cout << std::endl; // Ends the output line.
    }
}