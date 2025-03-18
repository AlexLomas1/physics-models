#include <iostream>
#include <cmath>

#define pi 3.14159265358979323846 

/* Note that while this is called orbital_engine, currently it is little more than a fancy circle 
drawer. This is done to test that frontend and the communication between the ends work as intented. */

int main() {
    float earth_x;
    float earth_y;
    float earth_angular_v = 2 * pi;
    
    for (int t=0; t <= 1000; t++) {
        // Parametric equation used to draw circular orbits.
        earth_x = sin(earth_angular_v * t/(50*pi));
        earth_y = cos(earth_angular_v * t/(50*pi));

        // Print new coordinates so Python file can read them.
        std::cout << earth_x << " " << earth_y << std::endl;
    }
}