#include <iostream>
#include <cmath>
#include <random>

int main() {
    int N; // Number of particles not yet decayed.
    int decayed; // Number of particles decayed in one run.
    float decay_const;

    std::cin >> N;
    std::cin >> decay_const;

    std::random_device rd; // Generates a seed for the (pseudo-)random number generator.
    std::mt19937 gen(rd()); // Mersenne Twister generator, uses rd() as a seed.
    std::uniform_real_distribution<> dis(0.0, 1.0);

    while (N > 0) {
        decayed = 0;
        for (int i=0; i < N; i++) {
            // Generates random number from 0 to 1.
            double r = dis(gen);
            if (r < decay_const) {
                decayed +=1;
            }
        }
        N -= decayed;
        std::cout << N << std::endl;
    }
}