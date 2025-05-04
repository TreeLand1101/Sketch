#include <iostream>
#include <cstdint>
#include <ctime>
#include <cstdlib>
#include <emmintrin.h>
#include "hash.h"
#include "Util.h"

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    constexpr int NUM_TESTS = 100;
    constexpr int NUM_SEEDS = 4;

    int fail_count = 0;

    for (int t = 0; t < NUM_TESTS; ++t) {
        std::cout << "=== Test " << (t + 1) << " ===" << std::endl;

        // 1) generate 4 random seeds [0,255]
        uint32_t seeds[NUM_SEEDS];
        std::cout << "seed: (";
        for (int i = 0; i < NUM_SEEDS; ++i) {
            seeds[i] = std::rand() % 256;
            std::cout << seeds[i];
            if (i < NUM_SEEDS - 1) std::cout << ", ";
        }
        std::cout << ")" << std::endl;

        // 2) fill data buffer with random bytes
        TUPLES data;
        for (size_t i = 0; i < TUPLES_LEN; ++i) {
            data[i] = static_cast<uint8_t>(std::rand() & 0xFF);
        }

        // 3) compute scalar hashes
        uint32_t h_scalar[NUM_SEEDS];
        std::cout << "scalar: (";
        for (int i = 0; i < NUM_SEEDS; ++i) {
            h_scalar[i] = hash(data, seeds[i]);
            std::cout << "0x" << std::hex << h_scalar[i] << std::dec;
            if (i < NUM_SEEDS - 1) std::cout << ", ";
        }
        std::cout << ")" << std::endl;

        // 4) compute SIMD hash
        __m128i simdHash = hash_sse2(data, seeds[0], seeds[1], seeds[2], seeds[3]);

        // 5) extract SIMD results
        alignas(16) uint32_t simdResults[NUM_SEEDS];
        _mm_store_si128(reinterpret_cast<__m128i*>(simdResults), simdHash);

        // 6) compare & report
        bool passed = true;
        std::cout << "simd  : (";
        for (int i = 0; i < NUM_SEEDS; ++i) {
            std::cout << "0x" << std::hex << simdResults[i] << std::dec;
            if (simdResults[i] != h_scalar[i]) {
                std::cout << " MISMATCH!";
                passed = false;
                fail_count++;
            }
            if (i < NUM_SEEDS - 1) std::cout << ", ";
        }
        std::cout << ")" << std::endl;

        if (passed) {
            std::cout << "Result: PASS" << std::endl << std::endl;
        } 
        else {
            std::cout << "Result: FAIL" << std::endl << std::endl;
        }
    }

    std::cout << "==============================" << std::endl;
    if (fail_count == 0) {
        std::cout << "All tests PASSED." << std::endl;
    } 
    else {
        std::cout << "Tests FAILED." << std::endl;
        std::cout << "TOTAL FAILS = " << fail_count << std::endl;
    }

    return 0;
}
