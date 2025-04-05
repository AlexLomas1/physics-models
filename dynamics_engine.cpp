#include <iostream>
#include <cmath>

const float g = 9.81; // Gravitational field strenght of Earth
const float air_density = 1.225; // Density of air at sea level (kgm^-3)

class Projectile {
    public:
        double mass, area, drag_coeff, x, y, v_x, v_y, a_x, a_y;
    
        void init(double h, double u, double angle, double m, double A, double C) {
            y = h;
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
    // PROBLEM: How do I make sure it is always acting in direction opposite to v, as v is 
    // squared in equation?
    double F_x = 0.5 * air_density * v_x * v_x * drag_coeff * area;
    double F_y = 0.5 * air_density * v_y * v_y * drag_coeff * area;
    
    // Ensures acceleration is in opposite direction to velocity.
    if (v_x < 0) {
        a_x = F_x / mass;
    }
    else {
        a_x = -F_x / mass;
    }

    if (v_y < 0) {
        a_y = F_y / mass;
    }
    else {
        a_y = -F_y / mass;
    }

    // POTENTIAL PROBLEM: How do I prevent speed exceeding terminal velocity? Can drag force ever be
    // enough that the ball moves upwards?
    // Adds acceleration due to gravity.
    a_y = a_y - g;
}