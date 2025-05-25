#include <iostream>
#include <cmath>
#include <ctime>
#include <random>

int main() {
    int N; // Number of particles not yet decayed.
    int decayed; // Number of particles decayed in one run.
    float decay_const; // (s^-1)
    float dt; // Time step (s).

    std::cin >> N;
    std::cin >> decay_const;
    std::cin >> dt;

    // Calculates probability of a particle decaying in a time step as P = 1 - e^(-λΔt)
    float decay_prob = 1 - exp(-decay_const * dt);

    // Mersenne Twister generator, uses current time as a seed.
    std::mt19937 gen(static_cast<unsigned int>(std::time(nullptr))); 
    std::uniform_real_distribution<> dis(0.0, 1.0);

    // Repeats until all particles have decayed.
    while (N > 0) {
        decayed = 0;
        for (int i=0; i < N; i++) {
            // Generates random number from 0 to 1, normally distributed.
            double r = dis(gen);
            if (r < decay_prob) {
                decayed +=1;
            }
        }
        N -= decayed;
        std::cout << N << std::endl;
    }
}