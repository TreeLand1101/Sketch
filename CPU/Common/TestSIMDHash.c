#include <iostream>
#include <cstdint>
#include <emmintrin.h>
#include "hash.h"
#include "Util.h"

int main()
{
    // 測試資料
    TUPLES data;
    for (int i = 0; i < 8; ++i) {
        data[i] = i;
    }

    // 計算標量版本的 hash 值 (針對不同 seed)
    uint32_t h0 = hash(data, 0);
    uint32_t h1 = hash(data, 1);
    uint32_t h2 = hash(data, 2);
    uint32_t h3 = hash(data, 3);

    // 使用 SIMD 版本計算 hash (同時取得 4 個結果)
    __m128i simdHash = hash_sse2(data, 0, 1, 2, 3);

    // 將 SIMD 結果存入 4 個 32-bit 的陣列中
    uint32_t simdResults[4];
    _mm_store_si128(reinterpret_cast<__m128i*>(simdResults), simdHash);

    // 比對各個 seed 的結果是否一致
    bool allMatch = true;
    if (h0 != simdResults[0]) {
        std::cerr << "Seed 0 不匹配: scalar = " << h0 << ", SIMD = " << simdResults[0] << "\n";
        allMatch = false;
    }
    if (h1 != simdResults[1]) {
        std::cerr << "Seed 1 不匹配: scalar = " << h1 << ", SIMD = " << simdResults[1] << "\n";
        allMatch = false;
    }
    if (h2 != simdResults[2]) {
        std::cerr << "Seed 2 不匹配: scalar = " << h2 << ", SIMD = " << simdResults[2] << "\n";
        allMatch = false;
    }
    if (h3 != simdResults[3]) {
        std::cerr << "Seed 3 不匹配: scalar = " << h3 << ", SIMD = " << simdResults[3] << "\n";
        allMatch = false;
    }

    if (allMatch) {
        std::cout << "所有 hash 值匹配，測試通過！\n";
    } else {
        std::cerr << "測試失敗！\n";
    }

    return allMatch ? 0 : 1;
}
