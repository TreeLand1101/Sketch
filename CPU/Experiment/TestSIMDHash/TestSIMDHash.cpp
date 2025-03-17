#include <iostream>
#include <cstdint>
#include <emmintrin.h>
#include "hash.h"
#include "Util.h"

int main()
{
    // Test data
    TUPLES data;
    for (int i = 0; i < TUPLES_LEN; ++i) {
        data[i] = i;
    }

    // Compute hash values using the scalar version (for different seeds)
    uint32_t h0 = hash(data, 0);
    uint32_t h1 = hash(data, 1);
    uint32_t h2 = hash(data, 2);
    uint32_t h3 = hash(data, 3);

    // Compute hash values using the SIMD version (obtain 4 results simultaneously)
    __m128i simdHash = hash_sse2(data, 0, 1, 2, 3);

    // Store the SIMD results into a 4-element 32-bit array
    uint32_t simdResults[4];
    _mm_store_si128(reinterpret_cast<__m128i*>(simdResults), simdHash);

    // Compare the results for each seed to check if they match
    bool allMatch = true;
    if (h0 != simdResults[0]) {
        std::cerr << "Seed 0 mismatch: scalar = " << h0 << ", SIMD = " << simdResults[0] << "\n";
        allMatch = false;
    }
    if (h1 != simdResults[1]) {
        std::cerr << "Seed 1 mismatch: scalar = " << h1 << ", SIMD = " << simdResults[1] << "\n";
        allMatch = false;
    }
    if (h2 != simdResults[2]) {
        std::cerr << "Seed 2 mismatch: scalar = " << h2 << ", SIMD = " << simdResults[2] << "\n";
        allMatch = false;
    }
    if (h3 != simdResults[3]) {
        std::cerr << "Seed 3 mismatch: scalar = " << h3 << ", SIMD = " << simdResults[3] << "\n";
        allMatch = false;
    }

    if (allMatch) {
        std::cout << "All hash values match, test passed!\n";
    } else {
        std::cerr << "Test failed!\n";
    }

    return allMatch ? 0 : 1;
}
