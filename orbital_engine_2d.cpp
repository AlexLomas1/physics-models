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
        float semi_major_axis; // (m)
        float eccentricity; // Eccentricity of orbit
        float v_x; // Current velocity in x-direction (ms^-1)
        float v_y; // Current velocity in y-direction (ms^-1)
        float mass; // (kg)
        void init(float a, float b, float c) {
            semi_major_axis = a * AU;
            eccentricity = b;
            mass = c;

            /* All planets start at aphelion (max distance from sun), so as to produce an elliptical
            orbit. Aphelion modelled as being in positive y direction for all planets (for now at least). */
            x = 0;
            y = (1+eccentricity)*semi_major_axis; 
            // Initial velocity, which is also the minimum velocity, calculated using vis-viva equation.
            v_x = sqrt(G*(SunMass+mass)*((2/y)-(1/semi_major_axis)));
            v_y = 0;
        }
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

    /* Acceleration calculated using F = ma. It is negative as planet is being accelerated towards the
    the sun, positive would be accelerating the planet away. */
    a_x = -F_x / m;
    a_y = -F_y / m;
}

int main() {
    Planet planets[8]; // array to store Planet objects.

    // Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
    // init arguments: semi-major axis (in AU), eccentricity, mass

    Planet Mercury;
    Mercury.init(0.387, 0.206, 0.330 * pow(10,24));
    planets[0] = Mercury;

    Planet Venus;
    Venus.init(0.723, 0.007, 4.87 * pow(10,24));
    planets[1] = Venus;
    
    Planet Earth;
    Earth.init(1.000, 0.017, 5.97 * pow(10,24));
    planets[2] = Earth;

    Planet Mars;
    Mars.init(1.523, 0.094, 0.642 * pow(10,24));
    planets[3] = Mars;

    Planet Jupiter;
    Jupiter.init(5.204, 0.049, 1898 * pow(10,24));
    planets[4] = Jupiter;

    Planet Saturn;
    Saturn.init(9.583, 0.052, 568 * pow(10,24));
    planets[5] = Saturn;

    Planet Uranus;
    Uranus.init(19.191, 0.047, 86.8 * pow(10,24));
    planets[6] = Uranus;

    Planet Neptune;
    Neptune.init(30.07, 0.010, 102 * pow(10,24));
    planets[7] = Neptune;
    
    // May need to increase range of t to allow animation to last longer.
    for (int t=0; t <= 1000; t++) {
        for (int i=0; i < 8; i++) {
            float a_x, a_y;
            // a_x and a_y passed by reference.
            calc_acceleration(planets[i].mass, planets[i].x, planets[i].y, a_x, a_y);

            /* Updating planet's velocities and coordinates using Euler method. Time step is 1 day.
            Smaller time step would increase accuracy, but makes simulation slower. */
            planets[i].v_x += a_x * 86400; 
            planets[i].v_y += a_y * 86400;

            planets[i].x += planets[i].v_x * 86400;
            planets[i].y += planets[i].v_y * 86400;
            
            // Converts coordinates to AU and prints them so Python file can read them.
            std::cout << planets[i].x/AU << " " << planets[i].y/AU;
            /* Ensures each coordinate is seperated by a space, but that last coordinate doesn't have
            a trailing space. */
            if (i != 7) {
                std::cout << " ";
            } 
        }
        std::cout << std::endl; // Ends the output line.
    }
}