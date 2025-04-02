#include <iostream>
#include <cmath>

const double AU = 1.496e11; // Astronomical Unit in metres
const double G = 6.6743e-11; // Gravitational constant
const double SunMass = 1.989e30; // Mass of sun in kg

class Planet {
    public:
        double x, y, v_x, v_y, a_x, a_y, mass;

        void init(double a, double b, double c, double d, double e) {
            x = a;
            y = b;
            v_x = c;
            v_y = d;
            mass = e;
        }
};

void calc_acceleration(double m, double x, double y, double&a_x, double&a_y) {
    /* Force calculted using Newton's law of universal gravitation, with formula F = G * m1 * m2 / (r^2)
    where m1 and m2 are the masses of the two bodies and r is the distance between them. As the sun
    is fixed at [0, 0], the distance is just sqrt(x^2 + y^2). */
    double dist_squared = (x * x) + (y * y);
    double dist = sqrt(dist_squared);

    double F = G * m * SunMass / dist_squared;

    // Force resolved into x and y directions using ratios. 
    double F_x = F * x / dist;
    double F_y = F * y / dist;

    /* Acceleration calculated using F = ma. It is negative as planet is being accelerated towards the
    the sun, positive would be accelerating the planet away. */
    a_x = -F_x / m;
    a_y = -F_y / m;
}

int main() {
    Planet planets[8]; // array to store Planet objects.
    int planet_count = 0;
    int TimeStep;
    double x, y, v_x, v_y, mass;

    std::cin >> TimeStep;

    // Receives planetary data from Python file
    while (std::cin >> x >> y >> v_x >> v_y >> mass && planet_count < 8) {
        planets[planet_count].init(x, y, v_x, v_y, mass);
        calc_acceleration(planets[planet_count].mass, planets[planet_count].x, planets[planet_count].y, 
            planets[planet_count].a_x, planets[planet_count].a_y); // Calculating initial acceleration
        planet_count += 1;
    }
    
    while (true) {
        for (int i=0; i < planet_count; i++) {
            // Position updated ten times before new position is output in order to increase accuracy.
            for (int j=0; j < 10; j++) {
                double new_a_x, new_a_y;
                // Updating planet's position and velocity using Velocity Verlet integration.
                planets[i].x += planets[i].v_x * TimeStep + 0.5 * planets[i].a_x * TimeStep * TimeStep;
                planets[i].y += planets[i].v_y * TimeStep + 0.5 * planets[i].a_y * TimeStep * TimeStep;

                // Accelertion values passed by reference.
                calc_acceleration(planets[i].mass, planets[i].x, planets[i].y, new_a_x, new_a_y);

                planets[i].v_x += 0.5 * (planets[i].a_x + new_a_x) * TimeStep;
                planets[i].v_y += 0.5 * (planets[i].a_y + new_a_y) * TimeStep;

                planets[i].a_x = new_a_x;
                planets[i].a_y = new_a_y;

            }
            // Converts coordinates to AU and prints them so Python file can read them.
            std::cout << planets[i].x/AU << " " << planets[i].y/AU;
            /* Ensures each coordinate is seperated by a space, but that last coordinate doesn't have
            a trailing space. */
            if (i != planet_count - 1) {
                std::cout << " ";
            } 
        }
        std::cout << std::endl; // Ends the output line.
    }
}