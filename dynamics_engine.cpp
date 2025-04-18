#include <iostream>
#include <cmath>

const float g = 9.81; // Gravitational field strenght of Earth
const float air_density = 1.225; // Density of air at sea level (kgm^-3)

class Projectile {
    public:
        double mass, area, drag_coeff, x, y, prev_x, prev_y, v_x, v_y, a_x, a_y;
    
        void init(double h, double u, double angle, double m, double A, double C) {
            y = h;
            prev_y = -1; // Used to indicate projectile is in initial position.
            x = 0;
            angle = angle * 2 * M_PI / 360; // Converting angle to radians.
            v_x = u * cos(angle);
            v_y = u * sin(angle);
            mass = m;
            area = A;
            drag_coeff = C;
        }          
};

void calc_acceleration(double mass, double area, double v_x, double v_y, double drag_coeff, double& a_x, double& a_y) {
    // Calculating drag forces in x and y-directions using formula F = 0.5 * ρ * v^2 * C * A
    /* Speed used as v * v would always give positive direction, v * speed however gives direction of 
    velocity. So using v * speed, and multiplying force by -1, ensures force is in opposite direction to
    velocity. */
    double speed_x = sqrt(v_x * v_x);
    double speed_y = sqrt(v_y * v_y);

    double F_x = -0.5 * air_density * v_x * speed_x * drag_coeff * area;
    double F_y = -0.5 * air_density * v_y * speed_y * drag_coeff * area;
    
    // Calculting acceleration with F=ma
    a_x = F_x / mass;
    a_y = F_y / mass;

    // Adds acceleration due to gravity
    a_y -= g;
}

float linear_interpolation(float prev_x, float prev_y, float x, float y) {
    // Uses linear interpolation to estimate x value when y = 0.
    return ((prev_x * y) - (x * prev_y)) / (y - prev_y);
}

int main() {
    Projectile projectiles[2];
    int projectile_count = 0;
    double TimeStep, h, u, angle, mass, area, drag_coeff;

    std::cin >> TimeStep;

    // Receives projectile data from Python file.
    while (std::cin >> h >> u >> angle >> mass >> area >> drag_coeff && projectile_count < 2) {
        projectiles[projectile_count].init(h, u, angle, mass, area, drag_coeff);
        calc_acceleration(projectiles[projectile_count].mass, projectiles[projectile_count].area,
            projectiles[projectile_count].v_x, projectiles[projectile_count].v_y,
            projectiles[projectile_count].drag_coeff, projectiles[projectile_count].a_x, 
            projectiles[projectile_count].a_y); // Calculating initial acceleration
        projectile_count ++;
    }

    int projectiles_ended = 0;
    while (projectiles_ended < projectile_count) {
        for (int i=0; i < projectile_count; i++) {
            /* If projectile's motion has already ended (but the others' haven't), output last coordinates.
            prev_y == -1 indicates that this is the projectile's initial position, so doesn't stop if 
            projectile starts at [0, 0]. */
            if (projectiles[i].y <= 0 && projectiles[i].prev_y != -1) {
                std::cout << projectiles[i].x << " " << 0;
            }
            else {
                // Storing previous values
                projectiles[i].prev_x = projectiles[i].x;
                projectiles[i].prev_y = projectiles[i].y;

                // Calculating new position using velocity verlet integration.
                double new_a_x, new_a_y;
                projectiles[i].x += projectiles[i].v_x * TimeStep + 0.5 * projectiles[i].a_x * TimeStep * TimeStep;
                projectiles[i].y += projectiles[i].v_y * TimeStep + 0.5 * projectiles[i].a_y * TimeStep * TimeStep;

                calc_acceleration(projectiles[i].mass, projectiles[i].area, projectiles[i].v_x, projectiles[i].v_y,
                    projectiles[i].drag_coeff, new_a_x, new_a_y);
                
                projectiles[i].v_x += 0.5 * (projectiles[i].a_x + new_a_x) * TimeStep;
                projectiles[i].v_y += 0.5 * (projectiles[i].a_y + new_a_y) * TimeStep;

                projectiles[i].a_x = new_a_x;
                projectiles[i].a_y = new_a_y;

                if (projectiles[i].y <= 0) {
                    // Using linear interpolation to estimate x value when y = 0 (projectile hits ground)
                    projectiles[i].x = linear_interpolation(projectiles[i].prev_x, projectiles[i].prev_y, 
                        projectiles[i].x, projectiles[i].y);
                    projectiles[i].y = 0;
                    
                    std::cout << projectiles[i].x << " " << 0;
                    projectiles_ended ++;
                }
                else {
                    std::cout << projectiles[i].x << " " << projectiles[i].y;
                }

            }
            // Ensures that coordinates are seperated by spaces, but there are no trailing spaces.
            if (i != projectile_count - 1) {
                std::cout << " ";
            }
        }
        std::cout << std::endl; // Ends output line
    }
}