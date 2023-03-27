#include "customs/scenes/Scene1.h"
#include <chrono>
#include <iostream>


int main( )
{
    auto start = std::chrono::high_resolution_clock::now();
    Scene1::Render();
    std::cout << "Render execution time : " << std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::high_resolution_clock::now() - start).count() << "ms\n";
    return 0;
}
