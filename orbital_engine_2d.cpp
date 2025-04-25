#include <iostream>
#include <cmath>

const double AU = 1.496e11; // Astronomical Unit in metres
const double G = 6.6743e-11; // Gravitational constant (m^{3}kg^{-1}s^{-2})

class Planet {
    public:
        double x, y, v_x, v_y, a_x, a_y, temp_a_x, temp_a_y, mass;

        void init(double a, double b, double c, double d, double e) {
            x = a;
            y = b;
            v_x = c;
            v_y = d;
            mass = e;
            temp_a_x = 0;
            temp_a_y = 0;
        }

        void update_acceleration() {
            /* Updating current acceleration and resetting temp to zero for calculation of acceleration
            in next time step. */
            a_x = temp_a_x;
            a_y = temp_a_y;

            temp_a_x = 0;
            temp_a_y = 0;
        }
};

void calc_accelerations(Planet&planet_a, Planet&planet_b) {
    /* Force calculted using Newton's law of universal gravitation, with formula F = G * m1 * m2 / (r^2),
    where G is the gravitational constant, m1 and m2 are the masses of the two bodies and r is the
    distance between them. */
    double dist_squared = (planet_a.x - planet_b.x) * (planet_a.x - planet_b.x) + 
                        (planet_a.y - planet_b.y) * (planet_a.y - planet_b.y);
    double F = G * planet_a.mass * planet_b.mass / dist_squared;

    // Resolving force exerted on A into x and y directions. Force on B is just opposite in direction.
    double dist = sqrt(dist_squared);
    double F_x = F * (planet_b.x - planet_a.x) / dist;
    double F_y = F * (planet_b.y - planet_a.y) / dist;

    // Acceleration calculated using F = ma, opposite directions as planets are attracting each other.
    planet_a.temp_a_x += F_x / planet_a.mass;
    planet_a.temp_a_y += F_y / planet_a.mass;

    planet_b.temp_a_x += -F_x / planet_b.mass;
    planet_b.temp_a_y += -F_y / planet_b.mass;
}

int main() {
    Planet planets[16]; // array to store Planet objects. This includes the sun.
    int planet_count = 0;
    int TimeStep;
    double x, y, v_x, v_y, mass;

    std::cin >> TimeStep;

    // Receives planetary data from Python file
    while (std::cin >> x >> y >> v_x >> v_y >> mass && planet_count < 16) {
        planets[planet_count].init(x, y, v_x, v_y, mass);
        planet_count += 1;
    }

    // Calculating initial accelerations for planets.
    for (int i=0; i < planet_count; i++) {
        for (int j=i+1; j < planet_count; j++) {
            calc_accelerations(planets[i], planets[j]);
        }
        planets[i].update_acceleration();
    }
    
    // Updating each planet's position using Velocity Verlet integration
    while (true) {
        // Position updated 1000 times before new position is output to allow for shorter time steps.
        for (int k=0; k < 1000; k++) {
            // Updating each planet's current position
            for (int i=0; i < planet_count; i++) {
                planets[i].x += planets[i].v_x * TimeStep + 0.5 * planets[i].a_x * TimeStep * TimeStep;
                planets[i].y += planets[i].v_y * TimeStep + 0.5 * planets[i].a_y * TimeStep * TimeStep;
            }

            for (int i=0; i < planet_count; i++) {
                /* Summing planet's accelerations due to other bodies. Only need to check bodies at greater
                indexes as previous bodies would have already calculated their acceleration due to current
                body, and these would be the same as the previous bodies exerts on the current body, just
                opposite in direction, so these accelerations are added then to reduce redundant calculations. */
                for (int j=i+1; j < planet_count; j++) {
                    // Planet objects passed by reference.
                    calc_accelerations(planets[i], planets[j]);
                }
                planets[i].v_x += 0.5 * (planets[i].a_x + planets[i].temp_a_x) * TimeStep;
                planets[i].v_y += 0.5 * (planets[i].a_y + planets[i].temp_a_y) * TimeStep;

                planets[i].update_acceleration();
            }
        }
        // Outputting new positions
        for (int i=0; i < planet_count; i++) {
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